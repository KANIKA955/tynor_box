from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import svgwrite
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from .models import User, Design, CDR, BoxDesign
from .serializers import UserSerializer, DesignSerializer, CDRSerializer, MyTokenObtainPairSerializer, BoxDesignSerializer, LoginSerializer
from .utils import generate_box_layout
from django.views import View

# Custom JWT Token Obtain View
class TokenObtainPairViewCustom(TokenObtainPairView):
    """
    Custom view to obtain JWT access and refresh tokens.
    """
    serializer_class = MyTokenObtainPairSerializer

# User Management View
class UserView(APIView):
    """
    View for managing users (list and create).
    """
    def get(self, request):
        """
        List all users
        """
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch users: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Register a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"error": f"Failed to create user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Design Management View
class DesignView(APIView):
    """
    View for managing designs (list and create).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all designs
        """
        try:
            designs = Design.objects.all()
            serializer = DesignSerializer(designs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch designs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new design
        """
        serializer = DesignSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)  # Save the user as the creator
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"error": f"Failed to create design: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CDR Management View
class CDRView(APIView):
    """
    View for managing CDRs (list and create).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all CDRs
        """
        try:
            cdrs = CDR.objects.all()
            serializer = CDRSerializer(cdrs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch CDRs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new CDR
        """
        serializer = CDRSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(generated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"error": f"Failed to create CDR: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateSVGView(APIView):
    """
    A view to generate an SVG file and return it as a response.
    """
    def post(self, request):
        try:
            # Retrieve dimensions from the request data
            length = request.data.get("length")
            breadth = request.data.get("breadth")
            height = request.data.get("height")

            # Validate input dimensions
            if not all([length, breadth, height]):
                return JsonResponse({"error": "Length, breadth, and height are required."}, status=400)

            # Create an in-memory file to hold the SVG content
            buffer = BytesIO()

            # Create an SVG drawing object
            dwg = svgwrite.Drawing(size=("400px", "400px"), profile='tiny')

            # Add shapes and text to the SVG based on dimensions
            dwg.add(dwg.rect(insert=(10, 10), size=(length, height), fill='white', stroke='black'))
            dwg.add(dwg.rect(insert=(20 + length, 10), size=(breadth, height), fill='white', stroke='black'))
            dwg.add(dwg.text('Box Layout', insert=(50, 50), font_size="15px", fill="black"))

            # Write SVG data to the BytesIO buffer
            dwg.write(buffer)

            # Rewind the buffer to the beginning
            buffer.seek(0)

            # Return the SVG content as a response
            return Response(buffer.getvalue(), content_type='image/svg+xml', status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"Failed to generate SVG: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# CDR Report Generation View
class CDRReportView(APIView):
    """
    View to generate a CDR report for a specific design.
    """
    def get(self, request, design_id):
        try:
            # Fetch CDRs for the given design_id
            cdrs = CDR.objects.filter(design_id=design_id)

            # Create an in-memory file for the PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Set up PDF document title
            p.drawString(100, 750, f"CDR Report for Design ID: {design_id}")
            y_position = 700

            # Loop through each CDR record and add it to the PDF
            for cdr in cdrs:
                p.drawString(100, y_position, f"Specification: {cdr.specifications}")
                p.drawString(100, y_position - 20, f"Approval Status: {cdr.approval_status}")
                y_position -= 40

            # Finish the page and save the PDF
            p.showPage()
            p.save()

            # Rewind the buffer's file pointer to the beginning
            buffer.seek(0)

            # Create a response with the PDF content
            response = Response(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="cdr_report_{design_id}.pdf"'
            return response

        except Exception as e:
            return JsonResponse({"error": f"Failed to generate CDR report: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Box Design View
class BoxDesignView(APIView):
    """
    View for managing box designs (list and create).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all box designs
        """
        try:
            box_designs = BoxDesign.objects.all()
            serializer = BoxDesignSerializer(box_designs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch box designs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new box design
        """
        serializer = BoxDesignSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"error": f"Failed to create box design: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for user login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                # Return a success message and token (JWT could be added here)
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateBoxLayoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve dimensions from query parameters
            length = int(request.GET.get('L', 0))
            breadth = int(request.GET.get('B', 0))
            height = int(request.GET.get('H', 0))

            # Validate dimensions
            if length <= 0 or breadth <= 0 or height <= 0:
                return JsonResponse({
                    "error": "Invalid dimensions provided. Length, breadth, and height must be positive integers."
                }, status=400)

            # Generate the box layout SVG data
            svg_data = self.generate_box_data(length, breadth, height)

            # Save the SVG data to a BytesIO object
            output = BytesIO()
            output.write(svg_data.encode('utf-8'))
            output.seek(0)

            # Save the file to storage (e.g., default file system or cloud storage)
            file_path = default_storage.save('box_layout.svg', output)

            return JsonResponse({
                "message": "Box layout generated successfully.",
                "file_path": file_path
            })

        except Exception as e:
            return JsonResponse({
                "error": f"An error occurred: {str(e)}"
            }, status=400)

    def generate_box_data(self, length, breadth, height):
        """
        Generate the 2D box layout (SVG) based on the provided dimensions.
        """
        svg_template = f"""
        <svg width="{length * 2 + breadth * 2 + 20}" height="{breadth + height * 2 + 20}" xmlns="http://www.w3.org/2000/svg">
            <!-- Front Panel -->
            <rect x="{breadth}" y="0" width="{length}" height="{breadth}" fill="lightblue" stroke="black" />
            <!-- Back Panel -->
            <rect x="{breadth}" y="{breadth + height}" width="{length}" height="{breadth}" fill="lightgreen" stroke="black" />
            <!-- Top Panel -->
            <rect x="{breadth}" y="{breadth}" width="{length}" height="{height}" fill="lightyellow" stroke="black" />
            <!-- Bottom Panel -->
            <rect x="{breadth}" y="{breadth + height + breadth}" width="{length}" height="{height}" fill="orange" stroke="black" />
            <!-- Left Panel -->
            <rect x="0" y="{breadth}" width="{breadth}" height="{height}" fill="pink" stroke="black" />
            <!-- Right Panel -->
            <rect x="{length + breadth}" y="{breadth}" width="{breadth}" height="{height}" fill="lightgray" stroke="black" />
            <!-- Annotations -->
            <text x="{breadth + length / 2}" y="{breadth / 2}" text-anchor="middle" font-size="12" fill="black">Front Panel</text>
            <text x="{breadth + length / 2}" y="{breadth + height + breadth / 2}" text-anchor="middle" font-size="12" fill="black">Back Panel</text>
        </svg>
        """
        return svg_template