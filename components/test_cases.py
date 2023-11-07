from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Literal
from datetime import datetime

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

# Test 3
Difficulty = Literal["easy", "medium", "hard"]

class ThoughtAnswerResponse(BaseModel):
    thought: str
    answer: str
    difficulty: Difficulty

# Test 4
class CityResponse(BaseModel):
    city_name: str = Field(description="Name of the city")
    country: str = Field(description="country of the city")
    population_number: int = Field(description="number of inhabitants")
    local_currency: str = Field(description="local currency of the city")
    date_founded: datetime = Field(description="founding date of the city")
    
class Cities(BaseModel):
    cities: List[CityResponse]

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