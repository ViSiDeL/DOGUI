from pyautocad import Autocad, APoint
import pythoncom
from core import get_acad_instance, ensure_document
from draw import draw_line, draw_circle, draw_text
import io

# def test_autocad_connection():
#     pythoncom.CoInitialize()
#     try:
#         acad = Autocad(create_if_not_exists=True)
#         acad.visible = True
#         print("✅ Successfully connected to AutoCAD")

#         if acad.doc is None:
#             print("⚠️ No drawing open. Creating a new one...")
#             acad.app.Documents.Add()

#         # acad.model.AddLine(APoint(0, 0), APoint(100, 100))
#         # acad.model.AddLine(APoint(-1, -1), APoint(100, 100))
#         acad.model.AddText("AutoCAD Automation Ready", APoint(20, 20), 5)
#         acad.model.AddCircle(APoint(75, 75), 15)
#         acad.model.AddCircle(APoint(150, 150), 30)

#         print("✅ Drawing complete.")
#     except Exception as e:
#         print("❌ Error during automation:", e)

def main():
    acad = get_acad_instance()
    ensure_document(acad)

    draw_line(acad, (0, 0), (150, 150))
    draw_circle(acad, (75, 75), 30)
    draw_text(acad, "Welcome to AutoCAD Automation", (20, 20), 6)

    # path = io.generate_project_path("DemoProject")
    # io.save_drawing(acad, path)


    existing_file_path = r"C:\Users\sekani_b\Desktop\GitHub\Projects\IBM GEN AI\CAU-GenAI\cau-genai\dev_scripts\sekani_scripts\autocad_automation\test_drawing.dwg"

    try:
        io.open_drawing(acad, existing_file_path)

        # Now modify the opened file
        draw_text(acad, "Edited by automation", (10, 10), 5)
        draw_circle(acad, (50, 50), 20)
        draw_line(acad, (0, 0), (200, 200))

        print("✅ Drawing modifications complete.")

    except Exception as e:
        print(f"❌ Error while editing drawing: {e}")


if __name__ == "__main__":
    main()
    # test_autocad_connection()


