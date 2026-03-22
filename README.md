# Alchemical Operations MCP

Jungian alchemical operations as psychological transformation morphisms.

## Architecture

Three-layer Lushy pattern (0 LLM tokens):

**Layer 1: Operation Taxonomy**
- Complete olog of seven operations
- Keywords, structural patterns, transformation directionality
- Valid/invalid sequences and complementary pairs

**Layer 2: Detection Functions**  
- Keyword analysis (30% weight)
- Structural pattern analysis (50% weight)
- Transformation directionality (20% weight)
- Operation sequence detection

**Layer 3: Parameter Transformation**
- Transform aesthetic parameters through operations
- Numeric, categorical, and boolean transformations
- Operation sequencing with psychological arc interpretation

## Installation

```bash
pip install -e ".[dev]"
```

## Testing

```bash
./tests/run_tests.sh
```

## Usage

```python
# Detect operation
result = detect_alchemical_operation(
    text="Burn away bureaucracy, get to essentials"
)

# Transform parameters  
result = apply_alchemical_operation(
    unified_parameters={"visual_weight": 0.5},
    operation="calcinatio",
    intensity=0.7
)
```

## Cost Profile

- All layers: 0 tokens (fully deterministic)
