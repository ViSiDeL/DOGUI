"""
Create a single instance of the engine on app launch
Separate file so all other files can access it
"""

from models.engine import DesignEngine
import uuid

# generates randome engine id, starts engine
def create_engine():
    engine_id = uuid.uuid4().hex
    engine = DesignEngine(engine_id=engine_id, system_status="Initializing", active_module="None")
    
    print("\nDOGUI Design Engine Initialized:")
    print(f"   - Engine ID: {engine.engine_id}")
    print(f"   - Status: {engine.system_status}")
    print(f"   - Active Module: {engine.active_module}\n")

    return engine

design_engine = create_engine()
