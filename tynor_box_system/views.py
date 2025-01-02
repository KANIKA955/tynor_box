from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Design, CDR
from .serializers import DesignSerializer, CDRSerializer

@api_view(['POST'])
def create_design(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    # Ensure that only a designer can create a design
    if request.user.role != 'designer':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    # Get the uploaded file from the request
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    # Check for missing fields in the request
    name = request.data.get('name')
    version = request.data.get('version')
    dimensions = request.data.get('dimensions')
    material_specs = request.data.get('material_specs')

    if not name or not version or not dimensions or not material_specs:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Create a new design with the provided details and uploaded file
    try:
        design = Design.objects.create(
            user=request.user,
            name=name,
            version=version,
            dimensions=dimensions,
            material_specs=material_specs,
            file=file  # Save the uploaded file
        )
        # Serialize the design to return the details
        serializer = DesignSerializer(design)
        return JsonResponse({'message': 'Design created', 'design': serializer.data}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['PATCH'])
def approve_design(request, design_id):
    # Check if the user is a reviewer
    if request.user.role != 'reviewer':
        return Response({'error': 'Unauthorized'}, status=403)

    try:
        design = Design.objects.get(id=design_id)
    except Design.DoesNotExist:
        return Response({'error': 'Design not found'}, status=404)

    # Update the approval status of the design to 'approved'
    design.approval_status = 'approved'
    design.save()
    return Response({'message': 'Design approved'})


@api_view(['PATCH'])
def reject_design(request, design_id):
    # Check if the user is a reviewer
    if request.user.role != 'reviewer':
        return Response({'error': 'Unauthorized'}, status=403)

    try:
        design = Design.objects.get(id=design_id)
    except Design.DoesNotExist:
        return Response({'error': 'Design not found'}, status=404)

    # Update the approval status of the design to 'rejected'
    design.approval_status = 'rejected'
    design.save()
    return Response({'message': 'Design rejected'})


@api_view(['POST'])
def generate_cdr(request, design_id):
    # Attempt to fetch the design from the database
    try:
        design = Design.objects.get(id=design_id)
    except Design.DoesNotExist:
        return Response({'error': 'Design not found'}, status=404)

    # Create a CDR (Customer Design Report) for the design
    try:
        cdr = CDR.objects.create(
            design=design,
            generated_by=request.user,
            specifications=design.material_specs,
            approval_status=design.approval_status,
        )
        # Serialize the CDR to return the details
        serializer = CDRSerializer(cdr)
        return Response({'message': 'CDR report generated', 'cdr': serializer.data}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
