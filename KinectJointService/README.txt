INSTRUCCIONES - KinectJointService (Microservicio Base)

1. Requisitos:
   - .NET 6.0 SDK
   - Azure Kinect Sensor SDK
   - Azure Kinect Body Tracking SDK
   - Windows x64 con GPU compatible

2. Para ejecutar:
   - Abre terminal en esta carpeta
   - Ejecuta:
       dotnet restore
       dotnet build
       dotnet run

3. Endpoint disponible:
   http://localhost:5000/api/joints/live

4. Este microservicio entrega los joints del cuerpo en vivo como JSON.