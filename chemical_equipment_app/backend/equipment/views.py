from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.db.models import Count
import pandas as pd
import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime

from .models import Dataset, Equipment
from .serializers import (
    DatasetSerializer, DatasetSummarySerializer,
    EquipmentSerializer, UserSerializer, RegisterSerializer
)


class DatasetViewSet(viewsets.ModelViewSet):

    #View for Dataset CRUD operations
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated for production
    
    def get_queryset(self):
        """Return only last 5 datasets"""
        return Dataset.objects.all()[:5]
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generate and download PDF report for a dataset"""
        dataset = self.get_object()
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.filename}_{dataset.id}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
        )
        title = Paragraph(f"Equipment Analysis Report", title_style)
        elements.append(title)
        
        # Dataset Info
        info_style = styles['Normal']
        elements.append(Paragraph(f"<b>Dataset:</b> {dataset.filename}", info_style))
        elements.append(Paragraph(f"<b>Upload Date:</b> {dataset.upload_date.strftime('%Y-%m-%d %H:%M')}", info_style))
        elements.append(Paragraph(f"<b>Total Equipment:</b> {dataset.total_count}", info_style))
        elements.append(Spacer(1, 20))
        
        # Summary Statistics
        summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
        elements.append(summary_title)
        elements.append(Spacer(1, 10))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Average Flowrate', f"{dataset.avg_flowrate:.2f}"],
            ['Average Pressure', f"{dataset.avg_pressure:.2f}"],
            ['Average Temperature', f"{dataset.avg_temperature:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Equipment Type Distribution
        dist_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
        elements.append(dist_title)
        elements.append(Spacer(1, 10))
        
        dist_data = [['Equipment Type', 'Count']]
        for eq_type, count in dataset.equipment_type_distribution.items():
            dist_data.append([eq_type, str(count)])
        
        dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(dist_table)
        elements.append(Spacer(1, 20))
        
        # Equipment Data Table
        data_title = Paragraph("<b>Equipment Details</b>", styles['Heading2'])
        elements.append(data_title)
        elements.append(Spacer(1, 10))
        
        # Get equipment items
        equipment_items = dataset.equipment_items.all()[:20]  # Limit to first 20
        
        table_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for eq in equipment_items:
            table_data.append([
                eq.equipment_name[:20],  # Truncate long names
                eq.equipment_type,
                f"{eq.flowrate:.1f}",
                f"{eq.pressure:.1f}",
                f"{eq.temperature:.1f}"
            ])
        
        equipment_table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1*inch, 1*inch])
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(equipment_table)
        
        # Build PDF
        doc.build(elements)
        return response


@api_view(['POST'])
@permission_classes([AllowAny])  # Change to IsAuthenticated for production
def upload_csv(request):
    """
    Upload and process CSV file
    Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    csv_file = request.FILES['file']
    
    # Validate file type
    if not csv_file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be CSV format'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Read CSV file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        df = pd.read_csv(io_string)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response(
                {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        
        # Equipment type distribution
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Create Dataset
        dataset = Dataset.objects.create(
            user=request.user if request.user.is_authenticated else None,
            filename=csv_file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            equipment_type_distribution=type_distribution,
            data=df.to_dict('records')
        )
        
        # Create Equipment records
        equipment_objects = []
        for _, row in df.iterrows():
            equipment_objects.append(
                Equipment(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                )
            )
        
        Equipment.objects.bulk_create(equipment_objects)
        
        # Keep only last 5 datasets
        datasets = Dataset.objects.all()
        if datasets.count() > 5:
            datasets_to_delete = datasets[5:]
            for ds in datasets_to_delete:
                ds.delete()
        
        # Return response
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing CSV: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_summary(request, dataset_id):
    """Get summary statistics for a specific dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_history(request):
    """Get list of last 5 uploaded datasets"""
    datasets = Dataset.objects.all()[:5]
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by deleting token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


