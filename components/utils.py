import re
from pydantic import BaseModel, Field
from enum import Enum
from typing import Type, List, Literal
from datetime import datetime

# def create_pydantic_model_from_string(definitions_str):
#     # Split the string into blocks
#     blocks = definitions_str.strip().split('\n\n')

#     # Dictionary to hold dynamically created classes and also include the global context
#     created_classes = globals().copy()

#     # Pattern to detect class definition and BaseModel inheritance
#     class_pattern = re.compile(r'class\s+(\w+)\(BaseModel\):')

#     # Process each block to create classes
#     for block in blocks:
#         # Check if it is a Pydantic model definition
#         if "BaseModel" in block:
#             match = class_pattern.search(block)
#             if not match:
#                 raise ValueError("No valid Pydantic class found in the string.")
        
#         # Using exec to define classes from string
#         exec(block, created_classes)

#     # Extract the dynamically created classes
#     # Find the last defined class which should be the Pydantic model
#     pydantic_model = None
#     for name in reversed(list(created_classes.keys())):
#         if isinstance(created_classes[name], type) and issubclass(created_classes[name], BaseModel):
#             pydantic_model = created_classes[name]
#             break

#     if pydantic_model is None:
#         raise ValueError("No Pydantic model class was created.")

#     return pydantic_model

def create_pydantic_model_from_string(definitions_str):
    # Split the string into blocks
    blocks = definitions_str.strip().split('\n\n')

    # Dictionary to hold dynamically created classes and also include the global context
    created_classes = globals().copy()
    
    # Include Field in the context for exec
    created_classes['Field'] = Field
    # Include datetime in the context for exec
    created_classes['datetime'] = datetime
    # Include List in the context for exec
    created_classes['List'] = List
    # Include List in the context for exec
    created_classes['Literal'] = Literal
    

    # Process each block to create classes
    for block in blocks:
        # Using exec to define classes from string
        exec(block, created_classes)

    # Extract the dynamically created classes
    # Find the last defined class which should be the Pydantic model
    pydantic_model = None
    for name in reversed(list(created_classes.keys())):
        cls = created_classes[name]
        if isinstance(cls, type) and issubclass(cls, BaseModel) and cls is not BaseModel:
            pydantic_model = cls
            break

    if pydantic_model is None:
        raise ValueError("No Pydantic model class was created.")

    return pydantic_model

if __name__ == "__main__":
    definitions_str = """
# Enums
class Weapon(str, Enum):
    sword = "sword"
    axe = "axe"
    mace = "mace"
    spear = "spear"
    bow = "bow"
    crossbow = "crossbow"

class Armor(str, Enum):
    leather = "leather"
    chainmail = "chainmail"
    plate = "plate"

# Pydantic model
class Character(BaseModel):
    name: str
    age: int
    armor: Armor
    weapon: Weapon
    strength: int
"""

    # Create the classes from the definition string
    class_instance = create_pydantic_model_from_string(definitions_str)

    print(class_instance)