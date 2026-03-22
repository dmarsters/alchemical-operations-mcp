"""
Alchemical Operations MCP Server

Three-layer architecture:
- Layer 1: YAML olog taxonomy (0 tokens)
- Layer 2: Detection functions (0 tokens, deterministic)
- Layer 3: Transformation functions (0 tokens, deterministic morphisms)
"""

from fastmcp import FastMCP
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import re

# Initialize FastMCP server
mcp = FastMCP("alchemical-operations")

# Load taxonomy
TAXONOMY_PATH = Path(__file__).parent / "ologs" / "alchemical-operations.olog.yaml"
with open(TAXONOMY_PATH, 'r') as f:
    TAXONOMY = yaml.safe_load(f)


# ==============================================================================
# LAYER 2: DETECTION FUNCTIONS (0 tokens - deterministic)
# ==============================================================================

def _detect_alchemical_operation(
    text: str,
    detection_mode: str = "comprehensive"
) -> Dict[str, Any]:
    """Core detection logic - exposed for testing."""
    text_lower = text.lower()
    
    scores = {}
    weights = TAXONOMY["detection_weights"]
    
    for op_name, op_data in TAXONOMY["operations"].items():
        keyword_score = 0.0
        structural_score = 0.0
        directional_score = 0.0
        
        # Keyword matching
        all_keywords = (
            op_data["keywords"]["primary"] +
            op_data["keywords"]["secondary"] +
            op_data["keywords"]["emotional"]
        )
        matches = sum(1 for kw in all_keywords if kw.lower() in text_lower)
        keyword_score = min(1.0, matches / 3.0)
        
        # Structural pattern matching
        for pattern_obj in op_data["structural_patterns"]:
            if pattern_obj["pattern"].lower() in text_lower:
                structural_score = max(structural_score, pattern_obj["weight"])
        
        # Directional analysis
        direction = op_data["transformation_direction"]
        from_words = direction["from"].lower().split(", ")
        to_words = direction["to"].lower().split(", ")
        
        from_matches = sum(1 for word in from_words if word in text_lower)
        to_matches = sum(1 for word in to_words if word in text_lower)
        
        if from_matches > 0 or to_matches > 0:
            directional_score = 0.5 + (to_matches / max(len(to_words), 1)) * 0.5
        
        # Weighted total
        total_score = (
            keyword_score * weights["keyword_match"] +
            structural_score * weights["structural_pattern"] +
            directional_score * weights["transformation_direction"]
        )
        
        scores[op_name] = {
            "total": total_score,
            "keyword": keyword_score,
            "structural": structural_score,
            "directional": directional_score
        }
    
    # Find top operation
    top_op = max(scores.items(), key=lambda x: x[1]["total"])
    
    result = {
        "primary_operation": top_op[0],
        "confidence": top_op[1]["total"],
        "element": TAXONOMY["operations"][top_op[0]]["element"],
        "description": TAXONOMY["operations"][top_op[0]]["description"]
    }
    
    if detection_mode == "comprehensive":
        result["all_scores"] = scores
        result["detection_breakdown"] = top_op[1]
    
    return result


@mcp.tool()
def detect_alchemical_operation(
    text: str,
    detection_mode: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Detect which alchemical operation best matches input text.
    
    Args:
        text: Input text to analyze
        detection_mode: "simple" (just operation) or "comprehensive" (full scores)
    
    Returns:
        Detection results with primary operation, confidence, and scores
    """
    return _detect_alchemical_operation(text, detection_mode)


def _list_all_operations() -> Dict[str, Any]:
    """Core list logic - exposed for testing."""
    operations = {}
    for op_name, op_data in TAXONOMY["operations"].items():
        operations[op_name] = {
            "name": op_data["name"],
            "element": op_data["element"],
            "description": op_data["description"],
            "psychological_process": op_data["psychological_process"]
        }
    
    return {
        "operations": operations,
        "count": len(operations)
    }


@mcp.tool()
def list_all_operations() -> Dict[str, Any]:
    """List all seven alchemical operations with descriptions."""
    return _list_all_operations()


def _get_operation_details(operation_name: str) -> Dict[str, Any]:
    """Core details logic - exposed for testing."""
    if operation_name not in TAXONOMY["operations"]:
        return {"error": f"Operation '{operation_name}' not found"}
    
    return TAXONOMY["operations"][operation_name]


@mcp.tool()
def get_operation_details(operation_name: str) -> Dict[str, Any]:
    """Get complete details for a specific operation."""
    return _get_operation_details(operation_name)


# Additional Layer 2 tools...

@mcp.tool()
def get_complementary_pairs() -> Dict[str, Any]:
    """Get complementary operation pairs."""
    return TAXONOMY["complementary_pairs"]


@mcp.tool()
def get_valid_sequences() -> Dict[str, Any]:
    """Get psychologically valid operation sequences."""
    return TAXONOMY["valid_sequences"]


@mcp.tool()
def analyze_operation_sequence(
    sequence: List[str]
) -> Dict[str, Any]:
    """Analyze whether a sequence is psychologically valid."""
    # Check if sequence matches any valid pattern
    for seq_name, seq_data in TAXONOMY["valid_sequences"].items():
        if sequence == seq_data["sequence"]:
            return {
                "valid": True,
                "sequence_name": seq_name,
                "description": seq_data["description"],
                "psychological_meaning": seq_data["psychological_meaning"]
            }
    
    # Check if sequence matches any invalid pattern
    for seq_name, seq_data in TAXONOMY["invalid_sequences"].items():
        if sequence == seq_data["sequence"]:
            return {
                "valid": False,
                "sequence_name": seq_name,
                "description": seq_data["description"],
                "reason": seq_data["reason"]
            }
    
    return {
        "valid": "unknown",
        "message": "Sequence not in predefined patterns"
    }


# ==============================================================================
# LAYER 3: TRANSFORMATION FUNCTIONS (0 tokens - deterministic morphisms)
# ==============================================================================

def _apply_alchemical_operation(
    parameters: Dict[str, float],
    operation: str,
    intensity: float = 0.5
) -> Dict[str, Any]:
    """Core transformation logic - exposed for testing."""
    if operation not in TAXONOMY["operations"]:
        return {"error": f"Operation '{operation}' not found"}
    
    op_data = TAXONOMY["operations"][operation]
    transformed = parameters.copy()
    transformations = []
    
    for param_name, param_value in parameters.items():
        if isinstance(param_value, (int, float)):
            # Numeric transformation
            new_value = _transform_numeric_parameter(
                param_name, param_value, operation, intensity
            )
            transformed[param_name] = new_value
            transformations.append({
                "parameter": param_name,
                "original": param_value,
                "transformed": new_value,
                "delta": new_value - param_value
            })
    
    return {
        "operation": operation,
        "intensity": intensity,
        "original_parameters": parameters,
        "transformed_parameters": transformed,
        "transformations": transformations,
        "visual_guidance": op_data["visual_parameters"]
    }


@mcp.tool()
def apply_alchemical_operation(
    parameters: Dict[str, float],
    operation: str,
    intensity: float = 0.5
) -> Dict[str, Any]:
    """
    Apply alchemical operation to transform visual parameters.
    
    Args:
        parameters: Dict of parameter names to values (0.0-1.0)
        operation: Which operation to apply (calcinatio, solutio, etc.)
        intensity: How strongly to apply (0.0-1.0, default 0.5)
    
    Returns:
        Transformation results with original and new parameter values
    """
    return _apply_alchemical_operation(parameters, operation, intensity)


def _transform_numeric_parameter(
    param_name: str,
    value: float,
    operation: str,
    intensity: float
) -> float:
    """Transform a numeric parameter based on operation."""
    # Operation-specific transformations
    transformations = {
        "calcinatio": {
            "visual_weight": lambda v: v + (1.0 - v) * intensity * 0.5,
            "temperature": lambda v: v + (1.0 - v) * intensity * 0.7,
            "complexity": lambda v: v - v * intensity * 0.4,
            "contrast": lambda v: v + (1.0 - v) * intensity * 0.6
        },
        "solutio": {
            "boundary_clarity": lambda v: v - v * intensity * 0.5,
            "separation": lambda v: v - v * intensity * 0.6,
            "fluidity": lambda v: v + (1.0 - v) * intensity * 0.7,
            "clarity": lambda v: v - v * intensity * 0.4
        },
        "coagulatio": {
            "density": lambda v: v + (1.0 - v) * intensity * 0.6,
            "structure": lambda v: v + (1.0 - v) * intensity * 0.7,
            "materiality": lambda v: v + (1.0 - v) * intensity * 0.6,
            "form_definition": lambda v: v + (1.0 - v) * intensity * 0.5
        },
        "sublimatio": {
            "weight": lambda v: v - v * intensity * 0.6,
            "lightness": lambda v: v + (1.0 - v) * intensity * 0.7,
            "refinement": lambda v: v + (1.0 - v) * intensity * 0.6,
            "clarity": lambda v: v + (1.0 - v) * intensity * 0.5
        },
        "mortificatio": {
            "darkness": lambda v: v + (1.0 - v) * intensity * 0.7,
            "vitality": lambda v: v - v * intensity * 0.8,
            "entropy": lambda v: v + (1.0 - v) * intensity * 0.6,
            "weight": lambda v: v + (1.0 - v) * intensity * 0.4
        },
        "separatio": {
            "boundary_clarity": lambda v: v + (1.0 - v) * intensity * 0.7,
            "separation": lambda v: v + (1.0 - v) * intensity * 0.8,
            "definition": lambda v: v + (1.0 - v) * intensity * 0.6,
            "contrast": lambda v: v + (1.0 - v) * intensity * 0.5
        },
        "coniunctio": {
            "integration": lambda v: v + (1.0 - v) * intensity * 0.8,
            "balance": lambda v: v + (1.0 - v) * intensity * 0.7,
            "harmony": lambda v: v + (1.0 - v) * intensity * 0.7,
            "wholeness": lambda v: v + (1.0 - v) * intensity * 0.8
        }
    }
    
    if operation in transformations and param_name in transformations[operation]:
        return max(0.0, min(1.0, transformations[operation][param_name](value)))
    
    return value


def _apply_operation_sequence(
    parameters: Dict[str, float],
    sequence: List[str],
    intensity: float = 0.5
) -> Dict[str, Any]:
    """Core sequence logic - exposed for testing."""
    current_params = parameters.copy()
    step_results = []
    
    for i, operation in enumerate(sequence):
        result = _apply_alchemical_operation(current_params, operation, intensity)
        step_results.append({
            "step": i + 1,
            "operation": operation,
            "result": result
        })
        current_params = result["transformed_parameters"]
    
    return {
        "sequence": sequence,
        "step_results": step_results,
        "final_parameters": current_params,
        "total_steps": len(sequence)
    }


@mcp.tool()
def apply_operation_sequence(
    parameters: Dict[str, float],
    sequence: List[str],
    intensity: float = 0.5
) -> Dict[str, Any]:
    """Apply a sequence of operations in order."""
    return _apply_operation_sequence(parameters, sequence, intensity)


@mcp.tool()
def suggest_operation_for_transformation(
    current_state: str,
    desired_state: str
) -> Dict[str, Any]:
    """Suggest which operation to use based on desired transformation."""
    # Simple keyword matching for now
    suggestions = []
    
    current_lower = current_state.lower()
    desired_lower = desired_state.lower()
    
    for op_name, op_data in TAXONOMY["operations"].items():
        direction = op_data["transformation_direction"]
        from_desc = direction["from"].lower()
        to_desc = direction["to"].lower()
        
        # Check if current state matches "from" and desired matches "to"
        from_match = any(word in current_lower for word in from_desc.split(", "))
        to_match = any(word in desired_lower for word in to_desc.split(", "))
        
        if from_match and to_match:
            suggestions.append({
                "operation": op_name,
                "confidence": 0.8,
                "reasoning": f"Transforms from {from_desc} to {to_desc}"
            })
    
    if not suggestions:
        return {"suggestions": [], "message": "No clear operation match found"}
    
    return {"suggestions": suggestions}


@mcp.tool()
def get_operation_visual_parameters(operation: str) -> Dict[str, Any]:
    """Get visual parameters for an operation."""
    if operation not in TAXONOMY["operations"]:
        return {"error": f"Operation '{operation}' not found"}
    
    return {
        "operation": operation,
        "visual_parameters": TAXONOMY["operations"][operation]["visual_parameters"],
        "element": TAXONOMY["operations"][operation]["element"],
        "description": TAXONOMY["operations"][operation]["description"]
    }


# ==============================================================================
# STRATEGIC DOCUMENT ANALYSIS (Tomographic Domain Projection)
# ==============================================================================

STRATEGIC_PATTERNS = {
    "transformation_readiness": {
        "calcinatio": {
            "regex": r"\b(simplif(?:y|ied|ying|ication)|streamline|eliminate|reduce|remov(?:e|ing))\b",
            "threshold": 5,
            "confidence": 0.8,
            "categorical_family": "constraints"
        },
        "coagulatio": {
            "regex": r"\b(build|establish|formalize|structure|consolidate)\b",
            "threshold": 5,
            "confidence": 0.8,
            "categorical_family": "constraints"
        }
    },
    "integration_coherence": {
        "separatio": {
            "regex": r"\b(distinguish|differentiate|separate|specialize)\b",
            "threshold": 4,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        },
        "coniunctio": {
            "regex": r"\b(integrat(?:e|ed|ing|ion)|unif(?:y|ied|ying)|synerg(?:y|ies|istic)|merge|combine)\b",
            "threshold": 4,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        }
    },
    "energy_distribution": {
        "mortificatio": {
            "regex": r"\b(crisis|restructur(?:e|ing)|let go|discontinue)\b",
            "threshold": 3,
            "confidence": 0.85,
            "categorical_family": "constraints"
        },
        "sublimatio": {
            "regex": r"\b(elevate|aspir(?:e|ation)|transcend|exceed)\b",
            "threshold": 3,
            "confidence": 0.8,
            "categorical_family": "constraints"
        }
    },
    "boundary_dynamics": {
        "solutio_fluid": {
            "regex": r"\b(fluid|flexible|adapt(?:able|ive)|dissolve)\b",
            "threshold": 4,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        },
        "solutio_rigid": {
            "regex": r"\b(boundar(?:y|ies)|defined|rigid|fixed)\b",
            "threshold": 5,
            "confidence": 0.7,
            "categorical_family": "morphisms"
        }
    },
    "operational_sequencing": {
        "valid": {
            "analysis_before_synthesis": {
                "regex": r"\b(analyz(?:e|ing|sis)).{0,200}\b(synthesi[sz](?:e|ing)|creat(?:e|ing))\b",
                "confidence": 0.9
            },
            "dissolution_before_reformation": {
                "regex": r"\b(dissolve|deconstruct|break down).{0,200}\b(rebuild|reform|reconstitute)\b",
                "confidence": 0.85
            },
            "foundation_before_elaboration": {
                "regex": r"\b(foundation|base|core).{0,200}\b(elaborat(?:e|ion)|extend|expand)\b",
                "confidence": 0.8
            }
        },
        "invalid": {
            "premature_unification": {
                "regex": r"\b(integrat(?:e|ion)|unif(?:y|ication)).{0,100}(?!.*\b(after|following|once)\b.{0,50}\b(distinguish|separate|differentiate))",
                "warning": "Coniunctio before Separatio - premature integration",
                "confidence": 0.75
            },
            "premature_elevation": {
                "regex": r"\b(elevate|transcend|aspir).{0,100}(?!.*\b(foundation|ground|establish)\b)",
                "warning": "Sublimatio without foundation",
                "confidence": 0.7
            }
        },
        "categorical_family": "objects"
    }
}


def detect_transformation_readiness(text: str) -> Dict[str, Any]:
    """Detect Calcinatio vs Coagulatio patterns in strategy document."""
    import re
    
    patterns = STRATEGIC_PATTERNS["transformation_readiness"]
    
    calcinatio_matches = re.findall(patterns["calcinatio"]["regex"], text, re.IGNORECASE)
    coagulatio_matches = re.findall(patterns["coagulatio"]["regex"], text, re.IGNORECASE)
    
    findings = []
    
    if len(calcinatio_matches) >= patterns["calcinatio"]["threshold"]:
        findings.append({
            "dimension": "transformation_readiness",
            "pattern": "calcinatio_emphasis",
            "confidence": patterns["calcinatio"]["confidence"],
            "evidence": [f"Calcinatio indicators: {calcinatio_matches[:5]}"],
            "categorical_family": patterns["calcinatio"]["categorical_family"]
        })
    
    if len(coagulatio_matches) >= patterns["coagulatio"]["threshold"]:
        findings.append({
            "dimension": "transformation_readiness",
            "pattern": "coagulatio_emphasis",
            "confidence": patterns["coagulatio"]["confidence"],
            "evidence": [f"Coagulatio indicators: {coagulatio_matches[:5]}"],
            "categorical_family": patterns["coagulatio"]["categorical_family"]
        })
    
    return findings


def detect_integration_coherence(text: str) -> Dict[str, Any]:
    """Detect Separatio vs Coniunctio patterns."""
    import re
    
    patterns = STRATEGIC_PATTERNS["integration_coherence"]
    
    separatio_matches = re.findall(patterns["separatio"]["regex"], text, re.IGNORECASE)
    coniunctio_matches = re.findall(patterns["coniunctio"]["regex"], text, re.IGNORECASE)
    
    findings = []
    
    if len(separatio_matches) >= patterns["separatio"]["threshold"]:
        findings.append({
            "dimension": "integration_coherence",
            "pattern": "separatio_emphasis",
            "confidence": patterns["separatio"]["confidence"],
            "evidence": [f"Separatio indicators: {separatio_matches[:5]}"],
            "categorical_family": patterns["separatio"]["categorical_family"]
        })
    
    if len(coniunctio_matches) >= patterns["coniunctio"]["threshold"]:
        findings.append({
            "dimension": "integration_coherence",
            "pattern": "coniunctio_emphasis",
            "confidence": patterns["coniunctio"]["confidence"],
            "evidence": [f"Coniunctio indicators: {coniunctio_matches[:5]}"],
            "categorical_family": patterns["coniunctio"]["categorical_family"]
        })
    
    return findings


def detect_energy_distribution(text: str) -> Dict[str, Any]:
    """Detect Mortificatio vs Sublimatio patterns."""
    import re
    
    patterns = STRATEGIC_PATTERNS["energy_distribution"]
    
    mortificatio_matches = re.findall(patterns["mortificatio"]["regex"], text, re.IGNORECASE)
    sublimatio_matches = re.findall(patterns["sublimatio"]["regex"], text, re.IGNORECASE)
    
    findings = []
    
    if len(mortificatio_matches) >= patterns["mortificatio"]["threshold"]:
        findings.append({
            "dimension": "energy_distribution",
            "pattern": "mortificatio_emphasis",
            "confidence": patterns["mortificatio"]["confidence"],
            "evidence": [f"Mortificatio indicators: {mortificatio_matches[:3]}"],
            "categorical_family": patterns["mortificatio"]["categorical_family"]
        })
    
    if len(sublimatio_matches) >= patterns["sublimatio"]["threshold"]:
        findings.append({
            "dimension": "energy_distribution",
            "pattern": "sublimatio_emphasis",
            "confidence": patterns["sublimatio"]["confidence"],
            "evidence": [f"Sublimatio indicators: {sublimatio_matches[:3]}"],
            "categorical_family": patterns["sublimatio"]["categorical_family"]
        })
    
    return findings


def detect_boundary_dynamics(text: str) -> Dict[str, Any]:
    """Detect Solutio intensity (fluid vs rigid boundaries)."""
    import re
    
    patterns = STRATEGIC_PATTERNS["boundary_dynamics"]
    
    fluid_matches = re.findall(patterns["solutio_fluid"]["regex"], text, re.IGNORECASE)
    rigid_matches = re.findall(patterns["solutio_rigid"]["regex"], text, re.IGNORECASE)
    
    findings = []
    
    if len(fluid_matches) >= patterns["solutio_fluid"]["threshold"]:
        findings.append({
            "dimension": "boundary_dynamics",
            "pattern": "solutio_fluid",
            "confidence": patterns["solutio_fluid"]["confidence"],
            "evidence": [f"Fluid boundary indicators: {fluid_matches[:5]}"],
            "categorical_family": patterns["solutio_fluid"]["categorical_family"]
        })
    
    if len(rigid_matches) >= patterns["solutio_rigid"]["threshold"]:
        findings.append({
            "dimension": "boundary_dynamics",
            "pattern": "solutio_rigid",
            "confidence": patterns["solutio_rigid"]["confidence"],
            "evidence": [f"Rigid boundary indicators: {rigid_matches[:5]}"],
            "categorical_family": patterns["solutio_rigid"]["categorical_family"]
        })
    
    return findings


def detect_operational_sequencing(text: str) -> Dict[str, Any]:
    """Detect valid and invalid operation sequences."""
    import re
    
    patterns = STRATEGIC_PATTERNS["operational_sequencing"]
    findings = []
    
    # Check valid sequences
    for seq_name, seq_data in patterns["valid"].items():
        if re.search(seq_data["regex"], text, re.IGNORECASE | re.DOTALL):
            findings.append({
                "dimension": "operational_sequencing",
                "pattern": f"valid_{seq_name}",
                "confidence": seq_data["confidence"],
                "evidence": [f"Valid sequence: {seq_name.replace('_', ' ')}"],
                "categorical_family": patterns["categorical_family"]
            })
    
    # Check invalid sequences
    for seq_name, seq_data in patterns["invalid"].items():
        if re.search(seq_data["regex"], text, re.IGNORECASE | re.DOTALL):
            findings.append({
                "dimension": "operational_sequencing",
                "pattern": f"invalid_{seq_name}",
                "confidence": seq_data["confidence"],
                "evidence": [f"Warning: {seq_data['warning']}"],
                "categorical_family": patterns["categorical_family"]
            })
    
    return findings


def analyze_strategy_document(strategy_text: str) -> Dict[str, Any]:
    """
    Analyze strategy document through alchemical operations structural lens.
    
    Zero LLM cost - pure deterministic pattern matching.
    
    Args:
        strategy_text: Full text of strategy document
        
    Returns:
        Dictionary with findings including:
        - domain: "alchemical_operations"
        - findings: List of detected patterns
        - total_findings: Count
        - methodology: "deterministic_pattern_matching"
        - llm_cost_tokens: 0
    """
    all_findings = []

    # OPTIMIZE: Preprocess text once for all detectors
    text_lower = strategy_text.lower()
    
    # Run all detectors
    all_findings.extend(detect_transformation_readiness(text_lower))
    all_findings.extend(detect_integration_coherence(text_lower))
    all_findings.extend(detect_energy_distribution(text_lower))
    all_findings.extend(detect_boundary_dynamics(text_lower))
    all_findings.extend(detect_operational_sequencing(text_lower))
    
    return {
        "domain": "alchemical_operations",
        "findings": all_findings,
        "total_findings": len(all_findings),
        "methodology": "deterministic_pattern_matching",
        "llm_cost_tokens": 0
    }


@mcp.tool()
def analyze_strategy_document_tool(strategy_text: str) -> str:
    """
    Analyze a strategy document through alchemical operations structural lens.
    
    This is the tomographic domain projection tool - it projects strategic
    text through alchemical vocabulary to detect transformation patterns.
    
    Zero LLM cost - pure deterministic pattern matching.
    
    Args:
        strategy_text: Full text of strategy document
        
    Returns:
        JSON string with domain projection results
    """
    import json
    result = analyze_strategy_document(strategy_text)
    return json.dumps(result, indent=2)


# ==============================================================================
# PHASE 2.6 — RHYTHMIC PRESET INFRASTRUCTURE
# ==============================================================================
#
# 5D Morphospace for Alchemical Operations
# =========================================
# The seven Jungian operations occupy a continuous psychological transformation
# space.  Five orthogonal axes capture their full variation:
#
#   dissolution_cohesion  — 0.0 = solutio/fully fluid  ↔  1.0 = coagulatio/solid
#   ascent_descent        — 0.0 = mortificatio/underworld  ↔  1.0 = sublimatio/spirit
#   separation_union      — 0.0 = separatio/pure division  ↔  1.0 = coniunctio/union
#   heat_intensity        — 0.0 = cold/inert/death  ↔  1.0 = calcinatio/fire
#   transformation_depth  — 0.0 = surface change  ↔  1.0 = total self-dissolution
#
# Period design rationale:
#   14 — gap-filler 13–15  (between fractal(13) and nuclear/catastrophe/diatom(15))
#   19 — reinforces most resilient known gap-filler (18–20)
#   21 — reinforces growing 5-domain gap-filler (20–22)
#   27 — fills 25–29 region; tests competition with heraldic P27 / fractal P26
#   36 — new LCM(12,18) harmonic with diatom + nuclear; untested in catalog

import math as _math

ALCHEMICAL_PARAMETER_NAMES = [
    "dissolution_cohesion",
    "ascent_descent",
    "separation_union",
    "heat_intensity",
    "transformation_depth",
]

# Seven canonical states — one per operation, precisely placed in morphospace.
# Coordinates are designed to maximise inter-state Euclidean separation so that
# nearest-neighbor matching is unambiguous everywhere in the space.
ALCHEMICAL_CANONICAL_STATES = {
    "calcinatio": {
        # Fire: maximum heat, moderate cohesion (ash), slightly ascending, deep
        "dissolution_cohesion":  0.50,
        "ascent_descent":        0.60,
        "separation_union":      0.45,
        "heat_intensity":        0.95,
        "transformation_depth":  0.80,
    },
    "solutio": {
        # Water: near-total dissolution, descending, cool, moderate depth
        "dissolution_cohesion":  0.05,
        "ascent_descent":        0.25,
        "separation_union":      0.38,
        "heat_intensity":        0.20,
        "transformation_depth":  0.55,
    },
    "coagulatio": {
        # Earth: near-total solidification, heavy/descending, cool, structured
        "dissolution_cohesion":  0.92,
        "ascent_descent":        0.15,
        "separation_union":      0.55,
        "heat_intensity":        0.30,
        "transformation_depth":  0.65,
    },
    "sublimatio": {
        # Air: spirit ascending, moderate cohesion, warm, refined
        "dissolution_cohesion":  0.42,
        "ascent_descent":        0.95,
        "separation_union":      0.62,
        "heat_intensity":        0.40,
        "transformation_depth":  0.72,
    },
    "mortificatio": {
        # Nigredo: deepest descent, cold, isolated, most transformative
        "dissolution_cohesion":  0.32,
        "ascent_descent":        0.05,
        "separation_union":      0.18,
        "heat_intensity":        0.08,
        "transformation_depth":  0.97,
    },
    "separatio": {
        # Analysis: maximum division, neutral plane, moderate heat/depth
        "dissolution_cohesion":  0.55,
        "ascent_descent":        0.42,
        "separation_union":      0.05,
        "heat_intensity":        0.45,
        "transformation_depth":  0.50,
    },
    "coniunctio": {
        # Hierosgamos: maximum union, ascending, warm, very deep
        "dissolution_cohesion":  0.70,
        "ascent_descent":        0.72,
        "separation_union":      0.95,
        "heat_intensity":        0.62,
        "transformation_depth":  0.88,
    },
}

# Five rhythmic presets — each encodes a canonical alchemical transformation arc
ALCHEMICAL_RHYTHMIC_PRESETS = {
    "prima_materia": {
        "state_a": "calcinatio",
        "state_b": "solutio",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 14,
        "period": 14,
        "description": (
            "Fire burning to water — purifying heat collapses into fluid dissolution. "
            "The first matter reduced to ash, then dissolved: prima materia recovered."
        ),
        "period_rationale": (
            "Gap-filler 13–15; sits between fractal(13) and nuclear/catastrophe/diatom(15). "
            "Unique alchemical signature in the period landscape."
        ),
    },
    "solve_coagula": {
        "state_a": "solutio",
        "state_b": "coagulatio",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 19,
        "period": 19,
        "description": (
            "Dissolve and coagulate — the fundamental alchemical rhythm. "
            "Fluid dissolution giving way to crystalline solidification; "
            "the classical maxim repeated in triangular oscillation."
        ),
        "period_rationale": (
            "Reinforces the most resilient known gap-filler (18–20). "
            "Period 19 is among the most stable cross-domain attractors discovered."
        ),
    },
    "nigredo_albedo": {
        "state_a": "mortificatio",
        "state_b": "sublimatio",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 21,
        "period": 21,
        "description": (
            "Blackening rising to whitening — death of the old form ascending to "
            "purified spirit. The core arc of the opus: nigredo through albedo."
        ),
        "period_rationale": (
            "Reinforces 5-domain gap-filler (gap 20–22). "
            "A second domain coupling may amplify the Period 21 attractor from ~1.2% → 4%+."
        ),
    },
    "hierosgamos": {
        "state_a": "separatio",
        "state_b": "coniunctio",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 27,
        "period": 27,
        "description": (
            "Division seeking sacred union — the analytical cutting apart that "
            "prepares for the mystical marriage. Separatio as precondition of coniunctio."
        ),
        "period_rationale": (
            "Fills gap 25–29, adjacent to heraldic P27 and fractal P26. "
            "Tests attractor competition/strengthening in the 25–30 region."
        ),
    },
    "opus_magnum": {
        "state_a": "mortificatio",
        "state_b": "coniunctio",
        "pattern": "sinusoidal",
        "num_cycles": 2,
        "steps_per_cycle": 36,
        "period": 36,
        "description": (
            "The Great Work entire — from the deepest death and dissolution to the "
            "warmth of sacred wholeness. Maximum transformation depth traversing "
            "the full alchemical arc in one slow oscillation."
        ),
        "period_rationale": (
            "New LCM(12,18) = 36 harmonic with diatom + nuclear. "
            "Untested in the catalog; expected strong emergent LCM attractor."
        ),
    },
}

# Seven visual vocabulary types — one per operation, anchored at canonical coords.
# Keywords are optimised for ComfyUI / Stable Diffusion / DALL-E prompt injection.
ALCHEMICAL_VISUAL_TYPES = {
    "calcinatio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["calcinatio"],
        "keywords": [
            "white-hot purifying fire",
            "reduction to luminous ash",
            "alchemical athanor furnace",
            "fierce incandescent calcination",
            "scorched mineral residue",
            "essence stripped bare by flame",
            "radiant heat transformation",
        ],
    },
    "solutio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["solutio"],
        "keywords": [
            "fluid dissolution of form",
            "boundaries dissolving in water",
            "mercurial aqueous diffusion",
            "alchemical bath immersion",
            "transparent yielding surface",
            "cool reflective solution",
            "softened formless becoming",
        ],
    },
    "coagulatio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["coagulatio"],
        "keywords": [
            "dense crystalline solidification",
            "matter coagulating from solution",
            "heavy mineral deposit formation",
            "earthy alchemical salt",
            "structured geometric coagulum",
            "grounded solidified substance",
            "earth-weight materialisation",
        ],
    },
    "sublimatio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["sublimatio"],
        "keywords": [
            "ascending vapour sublimation",
            "spirit rising from dense matter",
            "alchemical albedo whitening",
            "refined ethereal luminosity",
            "upward spiral elevation",
            "purified transcendent air",
            "radiant aerial lightness",
        ],
    },
    "mortificatio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["mortificatio"],
        "keywords": [
            "nigredo blackening darkness",
            "putrefaction and primal decay",
            "deep underworld cold descent",
            "crow-black alchemical death",
            "rotting transformative nigredo",
            "prima materia chaos",
            "total dissolution of ego-form",
        ],
    },
    "separatio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["separatio"],
        "keywords": [
            "analytical separation of elements",
            "alchemical distillation layers",
            "sharp boundary discrimination",
            "extracting pure from impure",
            "clarified distinct substances",
            "precise elemental division",
            "discrimination of opposites",
        ],
    },
    "coniunctio": {
        "coords": ALCHEMICAL_CANONICAL_STATES["coniunctio"],
        "keywords": [
            "hierosgamos sacred marriage",
            "opposing forces uniting",
            "gold and silver conjunctio",
            "warm harmonious wholeness",
            "sun and moon conjunction",
            "integrated alchemical rebis",
            "the two-made-one",
        ],
    },
}


# --- helpers (private, 0 tokens) -------------------------------------------

def _generate_oscillation_alchemical(
    num_steps: int, num_cycles: float, pattern: str
) -> list:
    """Generate oscillation values in [0, 1] for alchemical preset trajectories."""
    vals = []
    for i in range(num_steps):
        t = (2 * _math.pi * num_cycles * i) / num_steps
        if pattern == "sinusoidal":
            v = 0.5 * (1 + _math.sin(t))
        elif pattern == "triangular":
            t_n = (num_cycles * i / num_steps) % 1.0
            v = 2 * t_n if t_n < 0.5 else 2 * (1 - t_n)
        elif pattern == "square":
            t_n = (num_cycles * i / num_steps) % 1.0
            v = 0.0 if t_n < 0.5 else 1.0
        else:
            v = 0.5 * (1 + _math.sin(t))
        vals.append(v)
    return vals


def _generate_alchemical_preset_trajectory(preset_name: str) -> list:
    """
    Generate complete trajectory for a Phase 2.6 alchemical preset.
    Returns list of state dicts (one per step) in 5D parameter space.
    """
    p   = ALCHEMICAL_RHYTHMIC_PRESETS[preset_name]
    sa  = ALCHEMICAL_CANONICAL_STATES[p["state_a"]]
    sb  = ALCHEMICAL_CANONICAL_STATES[p["state_b"]]
    total = p["num_cycles"] * p["steps_per_cycle"]
    alphas = _generate_oscillation_alchemical(total, p["num_cycles"], p["pattern"])
    return [
        {k: (1.0 - a) * sa[k] + a * sb[k] for k in ALCHEMICAL_PARAMETER_NAMES}
        for a in alphas
    ]


def _euclidean_dist_alchemical(state: dict, coords: dict) -> float:
    return _math.sqrt(
        sum((state.get(k, 0.5) - coords[k]) ** 2 for k in ALCHEMICAL_PARAMETER_NAMES)
    )


def _extract_alchemical_vocabulary(state: dict, strength: float = 1.0) -> dict:
    """
    Extract visual vocabulary for an alchemical state via nearest-neighbor matching.

    Finds the closest operation archetype in 5D morphospace and returns
    image-generation keywords weighted by proximity and strength.
    """
    best_name, best_dist = None, float("inf")
    for name, td in ALCHEMICAL_VISUAL_TYPES.items():
        d = _euclidean_dist_alchemical(state, td["coords"])
        if d < best_dist:
            best_dist, best_name = d, name

    td = ALCHEMICAL_VISUAL_TYPES[best_name]
    n_kw = max(2, round(strength * len(td["keywords"])))
    return {
        "nearest_type": best_name,
        "distance": round(best_dist, 4),
        "strength": strength,
        "keywords": td["keywords"][:n_kw],
        "all_types_distances": {
            name: round(_euclidean_dist_alchemical(state, d["coords"]), 4)
            for name, d in ALCHEMICAL_VISUAL_TYPES.items()
        },
    }


# ==============================================================================
# PHASE 2.6 TOOLS
# ==============================================================================

@mcp.tool()
def get_alchemical_canonical_states() -> Dict[str, Any]:
    """
    List all canonical alchemical states with their 5D morphospace coordinates.

    LAYER 1 TAXONOMY — 0 tokens

    Returns the seven operation archetypes as precise positions in a continuous
    psychological transformation space.  Axes:

      dissolution_cohesion  — 0.0=solutio (fully fluid) ↔ 1.0=coagulatio (solid)
      ascent_descent        — 0.0=mortificatio (underworld) ↔ 1.0=sublimatio (spirit)
      separation_union      — 0.0=separatio (pure division) ↔ 1.0=coniunctio (union)
      heat_intensity        — 0.0=cold/inert/death ↔ 1.0=calcinatio (maximum fire)
      transformation_depth  — 0.0=surface change ↔ 1.0=total self-dissolution
    """
    return {
        "parameter_names": ALCHEMICAL_PARAMETER_NAMES,
        "parameter_semantics": {
            "dissolution_cohesion": (
                "0.0=solutio maximum fluid dissolution, "
                "0.5=calcinatio/separatio balanced, "
                "1.0=coagulatio maximum solid crystallisation"
            ),
            "ascent_descent": (
                "0.0=mortificatio underworld/nigredo, "
                "0.5=separatio/calcinatio neutral plane, "
                "1.0=sublimatio spirit ascent/albedo"
            ),
            "separation_union": (
                "0.0=separatio pure analytical division, "
                "0.5=calcinatio/solutio neutral, "
                "1.0=coniunctio sacred marriage/wholeness"
            ),
            "heat_intensity": (
                "0.0=mortificatio cold death/inertia, "
                "0.5=sublimatio/separatio moderate, "
                "1.0=calcinatio maximum purifying fire"
            ),
            "transformation_depth": (
                "0.0=surface aesthetic change, "
                "0.5=solutio/separatio moderate, "
                "1.0=mortificatio/coniunctio total dissolution or union"
            ),
        },
        "canonical_states": ALCHEMICAL_CANONICAL_STATES,
        "state_descriptions": {
            "calcinatio":  "Fire: purification by burning, reduction to luminous ash/essence",
            "solutio":     "Water: dissolution of form, descending fluidity, cool release",
            "coagulatio":  "Earth: crystallisation, heavy matter taking form, grounded structure",
            "sublimatio":  "Air: elevation of spirit, ascending refinement, albedo whitening",
            "mortificatio":"Nigredo: death and decay, deepest underworld, cold total transformation",
            "separatio":   "Division: analytical cutting, discrimination of elements, clarification",
            "coniunctio":  "Hierosgamos: sacred marriage, sun-moon union, wholeness achieved",
        },
    }


@mcp.tool()
def get_alchemical_rhythmic_presets() -> Dict[str, Any]:
    """
    List all Phase 2.6 rhythmic presets with periods and transformation arcs.

    LAYER 1 TAXONOMY — 0 tokens

    Five canonical oscillation presets encoding classic alchemical transformation
    sequences, with periods designed for cross-domain resonance:

      prima_materia   — period 14  (gap-filler 13–15; unique alchemical signature)
      solve_coagula   — period 19  (reinforces resilient 4-domain gap-filler)
      nigredo_albedo  — period 21  (reinforces growing 5-domain gap-filler 20–22)
      hierosgamos     — period 27  (fills 25–29; tests heraldic P27 competition)
      opus_magnum     — period 36  (new LCM(12,18) with diatom + nuclear)
    """
    out = {}
    for name, p in ALCHEMICAL_RHYTHMIC_PRESETS.items():
        out[name] = {
            "period":           p["period"],
            "pattern":          p["pattern"],
            "state_a":          p["state_a"],
            "state_b":          p["state_b"],
            "num_cycles":       p["num_cycles"],
            "steps_per_cycle":  p["steps_per_cycle"],
            "total_steps":      p["num_cycles"] * p["steps_per_cycle"],
            "description":      p["description"],
            "period_rationale": p["period_rationale"],
        }
    return {
        "presets": out,
        "period_landscape": {
            "alchemical_periods": [14, 19, 21, 27, 36],
            "existing_domain_periods": {
                "microscopy":  [10, 16, 20, 24, 30],
                "nuclear":     [15, 18],
                "catastrophe": [15, 18, 20, 22, 25],
                "diatom":      [12, 15, 18, 20, 30],
                "heraldic":    [12, 16, 22, 25, 30],
                "fractal":     [13, 17, 22, 26, 32],
                "layering":    [11, 20, 23, 28, 40],
            },
            "gaps_filled":             ["Period 14: 13–15"],
            "attractor_reinforcements": ["Period 19 (gap 18–20)", "Period 21 (gap 20–22)"],
            "competition_tests":        ["Period 27: adjacent to heraldic P27 and fractal P26"],
            "new_lcm_harmonics":        ["Period 36: LCM(12,18) with diatom + nuclear"],
            "predictions": {
                "period_14": "Novel gap-filler; ~4–7% basin as unique alchemical signature",
                "period_19": "Reinforcement; may push existing 7.4% basin above 9%",
                "period_21": "Second coupling may amplify 1.2% → 4%+",
                "period_27": "Competition/merge with heraldic P27 (4.2%)",
                "period_36": "New LCM attractor; diatom+nuclear synchronisation ~4–8%",
            },
        },
    }


@mcp.tool()
def apply_alchemical_preset(
    preset_name: str,
    num_keyframes: int = 8,
) -> Dict[str, Any]:
    """
    Apply a Phase 2.6 alchemical preset and return sampled keyframe states.

    LAYER 2 DETERMINISTIC — 0 tokens

    Generates the complete oscillation trajectory for the requested preset,
    then samples evenly-spaced keyframes. Each keyframe includes a
    ``psychological_hint`` translating the 5D morphospace position back into
    the Jungian vocabulary of the dominant operation at that arc position.

    Args:
        preset_name:   prima_materia | solve_coagula | nigredo_albedo |
                       hierosgamos | opus_magnum
        num_keyframes: Number of evenly-spaced keyframes to return (2–32)

    Returns:
        Preset metadata, trajectory info, and sampled keyframes with
        dominant operation labels and psychological descriptors.
    """
    if preset_name not in ALCHEMICAL_RHYTHMIC_PRESETS:
        return {
            "error": f"Unknown preset '{preset_name}'",
            "available": list(ALCHEMICAL_RHYTHMIC_PRESETS.keys()),
        }

    num_keyframes = max(2, min(32, num_keyframes))
    p          = ALCHEMICAL_RHYTHMIC_PRESETS[preset_name]
    trajectory = _generate_alchemical_preset_trajectory(preset_name)
    total      = len(trajectory)

    indices = [round(i * (total - 1) / (num_keyframes - 1)) for i in range(num_keyframes)]

    keyframes = []
    for idx, step_idx in enumerate(indices):
        state = trajectory[step_idx]

        # Nearest canonical operation
        nearest_op = min(
            ALCHEMICAL_CANONICAL_STATES.items(),
            key=lambda kv: _euclidean_dist_alchemical(state, kv[1]),
        )
        op_name = nearest_op[0]
        op_dist = _euclidean_dist_alchemical(state, nearest_op[1])

        heat = state["heat_intensity"]
        heat_label = (
            "cold/inert"       if heat < 0.20 else
            "cool"             if heat < 0.40 else
            "moderate warmth"  if heat < 0.65 else
            "fierce heat"      if heat < 0.85 else
            "maximum calcinatio fire"
        )
        asc = state["ascent_descent"]
        asc_label = (
            "deep nigredo descent" if asc < 0.20 else
            "descending"           if asc < 0.40 else
            "neutral plane"        if asc < 0.60 else
            "ascending albedo"     if asc < 0.80 else
            "full sublimatio"
        )
        su = state["separation_union"]
        su_label = (
            "pure separatio"      if su < 0.20 else
            "tending to division" if su < 0.45 else
            "balanced tension"    if su < 0.60 else
            "tending to union"    if su < 0.80 else
            "full coniunctio"
        )

        keyframes.append({
            "keyframe_index":  idx,
            "trajectory_step": step_idx,
            "phase_fraction":  round(step_idx / (total - 1), 3),
            "parameters":      {k: round(v, 4) for k, v in state.items()},
            "psychological_hint": {
                "dominant_operation":      op_name,
                "distance_to_operation":   round(op_dist, 4),
                "heat_label":              heat_label,
                "ascent_label":            asc_label,
                "union_label":             su_label,
                "transformation_depth":    round(state["transformation_depth"], 3),
            },
        })

    return {
        "preset_name":           preset_name,
        "period":                p["period"],
        "pattern":               p["pattern"],
        "state_a":               p["state_a"],
        "state_b":               p["state_b"],
        "total_trajectory_steps": total,
        "description":           p["description"],
        "period_rationale":      p["period_rationale"],
        "num_keyframes":         num_keyframes,
        "keyframes":             keyframes,
        "usage_note": (
            "Pass keyframe['parameters'] to generate_alchemical_attractor_prompt(). "
            "Use keyframe['psychological_hint']['dominant_operation'] to select "
            "matching visual_parameters from get_operation_visual_parameters()."
        ),
    }


# ==============================================================================
# PHASE 2.7 — ATTRACTOR VISUALIZATION PROMPT GENERATION
# ==============================================================================

@mcp.tool()
def generate_alchemical_attractor_prompt(
    state: Optional[Dict[str, float]] = None,
    preset_name: Optional[str] = None,
    preset_keyframe: int = 0,
    mode: str = "composite",
    strength: float = 1.0,
) -> Dict[str, Any]:
    """
    Generate image-generation prompt from an alchemical attractor state.

    LAYER 3 SYNTHESIS — nearest-neighbor visual vocabulary extraction

    Translates a 5D alchemical morphospace position into concrete visual
    descriptors for ComfyUI, Stable Diffusion, or DALL-E. Prompts encode the
    Jungian psychological quality of the transformation stage — heat,
    dissolution, ascent, union — composable with any subject-matter domain.

    Accepts either:
      - A direct ``state`` dict (from apply_alchemical_preset keyframes)
      - A ``preset_name`` + ``preset_keyframe`` index to auto-sample

    Args:
        state:           Dict with ALCHEMICAL_PARAMETER_NAMES keys (overrides preset)
        preset_name:     Preset to sample when state is not provided
        preset_keyframe: Which keyframe to sample (0-indexed)
        mode:            "composite"  — single blended prompt
                         "split_view" — separate prompts per transformation axis
                         "sequence"   — three-keyframe arc progression
        strength:        Vocabulary blend weight [0.0–1.0]

    Returns:
        Generated prompt(s) with vocabulary analysis and symbolic commentary
    """
    # Resolve state
    if state is None:
        pname   = preset_name or "solve_coagula"
        kf_data = apply_alchemical_preset(pname, num_keyframes=max(8, preset_keyframe + 1))
        if "error" in kf_data:
            return kf_data
        kf_idx = min(preset_keyframe, len(kf_data["keyframes"]) - 1)
        state  = kf_data["keyframes"][kf_idx]["parameters"]
        source = f"preset '{pname}' keyframe {kf_idx}"
    else:
        source = "provided state"

    vocab   = _extract_alchemical_vocabulary(state, strength=strength)
    nearest = vocab["nearest_type"]
    kws     = vocab["keywords"]

    # Translate axes to evocative descriptors
    heat = state.get("heat_intensity", 0.5)
    heat_desc = (
        "cold mortificatio darkness"        if heat < 0.15 else
        "cool aqueous dissolution"          if heat < 0.35 else
        "moderate alchemical warmth"        if heat < 0.60 else
        "fierce calcinatio fire"            if heat < 0.85 else
        "maximum purifying incandescence"
    )
    asc = state.get("ascent_descent", 0.5)
    asc_desc = (
        "nigredo descent into underworld"   if asc  < 0.15 else
        "descending earthy gravitas"        if asc  < 0.40 else
        "tension between earth and air"     if asc  < 0.60 else
        "ascending albedo lightening"       if asc  < 0.85 else
        "full sublimatio elevation to spirit"
    )
    su = state.get("separation_union", 0.5)
    su_desc = (
        "pure separatio division"           if su   < 0.20 else
        "analytical discrimination at work" if su   < 0.45 else
        "balanced tension of opposites"     if su   < 0.60 else
        "coniunctio forces drawing together"if su   < 0.85 else
        "hierosgamos sacred marriage"
    )
    depth = state.get("transformation_depth", 0.5)
    depth_desc = (
        "surface transformation"                    if depth < 0.25 else
        "moderate psychological depth"              if depth < 0.55 else
        "deep self-dissolution"                     if depth < 0.80 else
        "total alchemical annihilation and rebirth"
    )

    if mode == "composite":
        prompt = (
            f"{', '.join(kws)}, {heat_desc}, {asc_desc}, "
            f"{su_desc}, {depth_desc}, "
            f"Jungian alchemical transformation, opus magnum imagery"
        )
        return {
            "mode":   "composite",
            "source": source,
            "prompt": prompt,
            "vocabulary_analysis": {
                "nearest_operation": nearest,
                "distance":          vocab["distance"],
                "keywords_used":     kws,
                "heat_descriptor":   heat_desc,
                "ascent_descriptor": asc_desc,
                "union_descriptor":  su_desc,
                "depth_descriptor":  depth_desc,
            },
        }

    elif mode == "split_view":
        mat_prompt   = f"{', '.join(kws[:3])}, {heat_desc}, alchemical material quality"
        space_prompt = f"{', '.join(kws[3:5])}, {asc_desc}, {su_desc}"
        depth_prompt = (
            f"{depth_desc}, transformation depth "
            f"{round(state.get('transformation_depth', 0.5), 2):.0%}, "
            f"Jungian depth psychology"
        )
        return {
            "mode":   "split_view",
            "source": source,
            "prompts": {
                "material_and_heat":      mat_prompt,
                "spatial_and_polarity":   space_prompt,
                "transformation_depth":   depth_prompt,
            },
            "combined_prompt": f"{mat_prompt}, {space_prompt}, {depth_prompt}",
            "vocabulary_analysis": {
                "nearest_operation": nearest,
                "distance":          vocab["distance"],
                "all_distances":     vocab["all_types_distances"],
            },
        }

    elif mode == "sequence":
        pname = preset_name or "solve_coagula"
        traj  = apply_alchemical_preset(pname, num_keyframes=3)
        if "error" in traj:
            return traj
        seq_prompts = []
        for kf in traj["keyframes"]:
            kv   = _extract_alchemical_vocabulary(kf["parameters"], strength=strength)
            hint = kf["psychological_hint"]
            seq_prompts.append({
                "keyframe":           kf["keyframe_index"],
                "phase":              kf["phase_fraction"],
                "nearest_operation":  kv["nearest_type"],
                "prompt": (
                    f"{', '.join(kv['keywords'][:4])}, {hint['heat_label']}, "
                    f"{hint['ascent_label']}, {hint['union_label']}"
                ),
            })
        return {
            "mode":            "sequence",
            "preset":          pname,
            "period":          ALCHEMICAL_RHYTHMIC_PRESETS[pname]["period"],
            "sequence_prompts": seq_prompts,
            "arc_description": ALCHEMICAL_RHYTHMIC_PRESETS[pname]["description"],
        }

    return {"error": f"Unknown mode '{mode}'. Use: composite, split_view, sequence"}


@mcp.tool()
def get_alchemical_domain_registry_config() -> Dict[str, Any]:
    """
    Export alchemical domain configuration for Tier 4D multi-domain composition.

    LAYER 1 TAXONOMY — 0 tokens

    Returns the complete domain specification required by domain_registry.py,
    enabling alchemical operations to participate in emergent attractor discovery
    alongside microscopy, nuclear, catastrophe, diatom, heraldic, fractal,
    and layering domains.

    Period design summary:
      14 — gap-filler 13–15 (unique alchemical signature)
      19 — reinforces most resilient known gap-filler (18–20)
      21 — reinforces growing 5-domain gap-filler (20–22)
      27 — tests attractor competition in 25–29 region
      36 — new LCM(12,18) harmonic with diatom + nuclear
    """
    presets_out = {}
    for name, p in ALCHEMICAL_RHYTHMIC_PRESETS.items():
        presets_out[name] = {
            "period":           p["period"],
            "pattern":          p["pattern"],
            "state_a_id":       p["state_a"],
            "state_b_id":       p["state_b"],
            "state_a_coords":   ALCHEMICAL_CANONICAL_STATES[p["state_a"]],
            "state_b_coords":   ALCHEMICAL_CANONICAL_STATES[p["state_b"]],
            "description":      p["description"],
            "period_rationale": p["period_rationale"],
        }

    return {
        "domain_id":    "alchemical",
        "display_name": "Alchemical Operations",
        "description": (
            "Jungian alchemical operations as psychological transformation morphisms — "
            "seven operations (calcinatio, solutio, coagulatio, sublimatio, mortificatio, "
            "separatio, coniunctio) mapped to a continuous 5D transformation space "
            "spanning heat, dissolution, ascent, union, and transformation depth"
        ),
        "mcp_server":          "alchemical-operations-mcp",
        "parameter_names":     ALCHEMICAL_PARAMETER_NAMES,
        "parameter_count":     len(ALCHEMICAL_PARAMETER_NAMES),
        "canonical_states":    ALCHEMICAL_CANONICAL_STATES,
        "canonical_state_count": len(ALCHEMICAL_CANONICAL_STATES),
        "presets":             presets_out,
        "periods":             [p["period"] for p in ALCHEMICAL_RHYTHMIC_PRESETS.values()],
        "visual_types": {
            name: {
                "coords":          td["coords"],
                "keyword_count":   len(td["keywords"]),
                "sample_keywords": td["keywords"][:3],
            }
            for name, td in ALCHEMICAL_VISUAL_TYPES.items()
        },
        "period_landscape_analysis": {
            "gaps_filled":              [14],
            "attractor_reinforcements": [19, 21],
            "competition_tests":        [27],
            "new_lcm_harmonics":        [36],
            "expected_interactions": {
                "unique_gap_filler":  "Period 14 between fractal(13) and nuclear(15)",
                "resilience_test":    "Period 19 — does alchemical coupling push 7.4% basin above 9%?",
                "gap_strengthening":  "Period 21 — second coupling may lift 1.2% → 4%+",
                "competition":        "Period 27 — adjacent to heraldic P27(4.2%); split or strengthen?",
                "new_lcm":            "Period 36 = LCM(12,18); diatom+nuclear three-domain sync",
            },
        },
        "composition_compatibility": {
            "high":     ["catastrophe", "fractal", "layering"],
            "moderate": ["diatom", "heraldic", "microscopy"],
            "note": (
                "Catastrophe theory shares singular-point transformation character; "
                "fractal shares complexity–hierarchy and dissolution–emergence dynamic; "
                "layering shares opacity and dissolution semantics. "
                "Nuclear aesthetics may suppress emergence (known nuclear effect applies)."
            ),
        },
        "registration_snippet": (
            "# In domain_registry.py initialize_registry():\n"
            "from alchemical_domain import register_alchemical_domain\n"
            "register_alchemical_domain()\n\n"
            "# Or pass get_alchemical_domain_registry_config() result directly:\n"
            "# config = alchemical_mcp.get_alchemical_domain_registry_config()\n"
            "# DOMAIN_REGISTRY['alchemical'] = DomainConfig(**config)"
        ),
    }


@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """Get complete server information including Phase 2.6 and 2.7 capabilities."""
    return {
        "name":         "alchemical-operations-mcp",
        "version":      "2.0.0",
        "description":  "Jungian alchemical operations as psychological transformation morphisms",
        "architecture": "three-layer deterministic + Phase 2.6 rhythmic presets + Phase 2.7 prompt generation",
        "layers": {
            "layer_1_taxonomy": {
                "description": "Pure categorical retrieval (0 tokens)",
                "tools": [
                    "list_all_operations",
                    "get_operation_details",
                    "get_complementary_pairs",
                    "get_valid_sequences",
                    "get_alchemical_canonical_states",
                    "get_alchemical_rhythmic_presets",
                    "get_alchemical_domain_registry_config",
                ],
            },
            "layer_2_computation": {
                "description": "Deterministic computation (0 tokens)",
                "tools": [
                    "detect_alchemical_operation",
                    "analyze_operation_sequence",
                    "apply_alchemical_operation",
                    "apply_operation_sequence",
                    "suggest_operation_for_transformation",
                    "analyze_strategy_document_tool",
                    "apply_alchemical_preset",
                ],
            },
            "layer_3_synthesis": {
                "description": "Synthesis preparation (Claude token cost)",
                "tools": [
                    "get_operation_visual_parameters",
                    "generate_alchemical_attractor_prompt",
                ],
            },
        },
        "phase_2_6": {
            "status": "complete",
            "canonical_states": list(ALCHEMICAL_CANONICAL_STATES.keys()),
            "presets": {
                name: {"period": p["period"], "pattern": p["pattern"], "description": p["description"]}
                for name, p in ALCHEMICAL_RHYTHMIC_PRESETS.items()
            },
            "periods": [14, 19, 21, 27, 36],
            "period_design": (
                "Gap-filling (14) + attractor reinforcement (19, 21) + "
                "competition test (27) + new LCM harmonic (36)"
            ),
        },
        "phase_2_7": {
            "status": "complete",
            "visual_types": list(ALCHEMICAL_VISUAL_TYPES.keys()),
            "prompt_modes": ["composite", "split_view", "sequence"],
            "target_generators": ["ComfyUI", "Stable Diffusion", "DALL-E"],
            "vocabulary_method": "Euclidean nearest-neighbor in 5D morphospace",
        },
        "existing_capabilities": {
            "operations_count":   len(TAXONOMY["operations"]),
            "complementary_pairs": len(TAXONOMY["complementary_pairs"]),
            "valid_sequences":     len(TAXONOMY["valid_sequences"]),
            "strategy_analysis":  True,
            "tomographic_projection": True,
        },
        "tier_4d_ready": True,
        "tier_4d_note": (
            "Call get_alchemical_domain_registry_config() for complete Tier 4D "
            "registration spec. Alchemical periods [14, 19, 21, 27, 36] target "
            "gap-filling, resilience reinforcement, competition testing, and "
            "new LCM harmonic discovery."
        ),
    }


def main():
    """Entry point for running the server."""
    mcp.run()


if __name__ == "__main__":
    main()
