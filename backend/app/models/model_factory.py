import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, Integer, String, Float, Numeric, Boolean, DateTime, ForeignKey
)
from datetime import datetime

# A mapping from string names to SQLAlchemy column types
COLUMN_TYPE_MAP = {
    "integer": Integer,
    "string": String,
    "float": Float,
    "numeric": Numeric,
    "boolean": Boolean,
    "datetime": DateTime,
}

def _create_class(db: SQLAlchemy, class_name: str, config: dict):
    """Internal function to create a single model class."""
    table_name = config.get("table_name")
    if not table_name:
        raise ValueError(f"Configuration for {class_name} must include a 'table_name'.")

    attributes = {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True)
    }

    for col_name, col_props in config.get("columns", {}).items():
        col_type_str = col_props.get("type")
        col_type = COLUMN_TYPE_MAP.get(col_type_str.lower())
        if not col_type:
            raise ValueError(f"Unsupported column type: {col_type_str}")

        type_args = col_props.get("args", [])
        
        col_kwargs = {
            "unique": col_props.get("unique", False),
            "nullable": col_props.get("nullable", True) 
        }

        # Handle default values
        default = col_props.get("default")
        if default is not None:
             if default == "datetime.utcnow":
                 col_kwargs["default"] = datetime.utcnow
             else:
                 col_kwargs["default"] = default
        
        # Handle foreign keys
        foreign_key = col_props.get("foreign_key")
        if foreign_key:
            attributes[col_name] = Column(col_type(*type_args), ForeignKey(foreign_key), **col_kwargs)
        else:
            attributes[col_name] = Column(col_type(*type_args), **col_kwargs)

    # Dynamically create the class inheriting from db.Model
    return type(class_name, (db.Model,), attributes)


def generate_models_from_directory(db: SQLAlchemy, directory: str):
    """
    Discovers all *.json files in a directory, generates SQLAlchemy models for them,
    and returns them in a dictionary.

    :param db: The SQLAlchemy instance.
    :param directory: The path to the directory containing model JSON configs.
    :return: A dictionary mapping model class names to the generated classes.
    """
    models = {}
    if not os.path.isdir(directory):
        print(f"Warning: Model directory not found at {directory}")
        return models

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            class_name = filename.replace(".json", "").capitalize()
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r') as f:
                try:
                    config = json.load(f)
                    model_class = _create_class(db, class_name, config)
                    models[class_name] = model_class
                    print(f"Successfully generated model: {class_name}")
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing {filename}: {e}")
    
    return models
