from client_kinect import KinectClient
from angle_calculator import AngleCalculator
from squat_tracker import SquatTracker
from clasificador import Clasificador
import cv2

client = KinectClient()
calculator = AngleCalculator()
tracker = SquatTracker()
clasificador = Clasificador()

while True:
    print("Solicitando imagen...")
    frame = client.get_render_frame()
    joints = client.get_joint_data()

    if frame is not None:
        print("Imagen recibida")
        if joints:
            print("Articulaciones detectadas")

            angles = calculator.calculate_both_knees(joints)
            left_angle = angles["left_knee_angle"]
            right_angle = angles["right_knee_angle"]
            diferencia = abs(left_angle - right_angle)

            tracker.update(left_angle)

            # Interpretaciones clínicas
            clasif_izq = clasificador.interpretar(left_angle)
            clasif_der = clasificador.interpretar(right_angle)

            # Mostrar ángulos y clasificación
            cv2.putText(frame, f"Izq: {left_angle:.1f}° {clasif_izq['nivel']}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Der: {right_angle:.1f}° {clasif_der['nivel']}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

            # Mostrar diferencia
            cv2.putText(frame, f"Diferencia: {diferencia:.1f}°", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # Diagnóstico general por diferencia
            if diferencia > 15:
                mensaje = " Diferencia significativa entre rodillas"
                color = (0, 0, 255)
            else:
                mensaje = " Rango funcional equilibrado"
                color = (0, 255, 0)

            cv2.putText(frame, mensaje, (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Contador de sentadillas
            cv2.putText(frame, f"Sentadillas: {tracker.get_count()}", (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            print("❌ No joints detectados")

        cv2.imshow("Kinect Render", frame)
    else:
        print("❌ No frame recibido")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
