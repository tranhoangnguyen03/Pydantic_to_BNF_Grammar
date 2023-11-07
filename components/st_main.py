import streamlit as st
from components.converter import pydantic_model_to_bnf
from components.utils import create_pydantic_model_from_string
from components.test_cases import Character, KnowledgeGraph, ThoughtAnswerResponse, Cities, CarAndOwner

test_cases_dict = {
    "Choose an example": "",

    "KnowledgeGraph": """
# Test 1
class Node(BaseModel):
    id: int
    label: str
    color: str


class Edge(BaseModel):
    source: int
    target: int
    label: str

class KnowledgeGraph(BaseModel):
    nodes: list[Node]= Field(default_factory=list)
    edges: list[Edge]= Field(default_factory=list)
""",

    "Character": '''
#Test 2
# Enums
class Weapon(str, Enum):
    sword = "sword"
    mace = "mace"

class Armor(str, Enum):
    leather = "leather"
    chainmail = "chainmail"

# Pydantic model
class Character(BaseModel):
    name: str
    age: int
    armor: Armor
    weapon: Weapon
''',
    
    "ThoughtAnswerResponse": '''
# Test 3
Difficulty = Literal["easy", "medium", "hard"]

class ThoughtAnswerResponse(BaseModel):
    thought: str
    answer: str
    difficulty: Difficulty
''',
    
    "Cities": '''
# Test 4
class CityResponse(BaseModel):
    city_name: str = Field(description="Name of the city")
    country: str = Field(description="country of the city")
    population_number: int = Field(description="number of inhabitants")
    local_currency: str = Field(description="local currency of the city")
    date_founded: datetime = Field(description="founding date of the city")
    
class Cities(BaseModel):
    cities: List[CityResponse]
''',
    
    "CarAndOwner": '''
# Test 5
class Owner(BaseModel):
  firstName: str
  age: int

class AudioFeature(BaseModel):
  brand: str
  speakers: int
  hasBluetooth: bool

class SafetyFeature(BaseModel):
  laneAssist: int

class PerformanceFeature(BaseModel):
  engine: str
  horsepower: int
 
class Features(BaseModel):
  audio: AudioFeature
  safety: SafetyFeature
  performance: PerformanceFeature

class Car(BaseModel):
  model: str
  year: int
  colors: list[str]
  features: Features

class CarAndOwner(BaseModel):
  car: Car
  owner: Owner
'''
}

def st_main():
    
    col_a, col_b = st.columns([2,8])
    with col_a:
        test_case_name = st.selectbox("Examples:", options=list(test_cases_dict.keys()), index=0)
        default_test_case = test_cases_dict[test_case_name]
    with col_b:
        input_ = st.text_area('Your Pydantic Class', value=default_test_case, height=400)
    
    submitted = st.button('Submit',use_container_width=True)
    
    if submitted:
        pydantic_class = create_pydantic_model_from_string(input_)
        
        bnf = pydantic_model_to_bnf(pydantic_class)
        
        col1, col2 = st.columns([4,6])
        
        with col1:
            st.code(input_, line_numbers=True)
        
        with col2:
            st.code(bnf.replace('\n', '  \n') , line_numbers=True)
