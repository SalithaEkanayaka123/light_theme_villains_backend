"""
FINAL COMPLETE VERSION - Comprehensive Training Data Generator
Generates 5000 samples with 47+ Java/Spring theories
WITH FORCED PATTERN SAMPLES and CORRECT PATTERN NAMES
"""

import pandas as pd
import numpy as np
from typing import List, Tuple

# --- Safe getter helper: prevents KeyError when a structural flag is missing ---
def get(row, key, default):
    """
    Safe accessor for pandas Series / dict-like row objects.
    Use get(row, 'colname', default) instead of row['colname'].
    """
    try:
        # For pandas Series
        return row[key]
    except Exception:
        # If key missing or other error, return default
        return default

def generate_comprehensive_training_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    ✅ FIXED: Generate training data with ONLY 20 metrics
    
    This matches what api_server.py returns - NO extra columns!
    
    Returns DataFrame with:
    - 20 code metric features (EXACTLY matching api_server.py)
    - patterns (comma-separated - 47 total theories)
    - vulnerability_type
    - severity
    """
    np.random.seed(42)

    # Initialize with random data - ONLY 20 METRICS
    data = {
        # Complexity metrics (3)
        'cyclomatic_complexity': np.random.randint(1, 50, n_samples),
        'cognitive_complexity': np.random.randint(1, 100, n_samples),
        'nesting_depth': np.random.randint(1, 10, n_samples),

        # Size metrics (4)
        'lines_of_code': np.random.randint(10, 1000, n_samples),
        'num_methods': np.random.randint(1, 50, n_samples),
        'num_classes': np.random.randint(1, 20, n_samples),
        'num_parameters': np.random.randint(0, 15, n_samples),

        # Quality metrics (3)
        'code_duplication': np.random.uniform(0, 0.5, n_samples),
        'test_coverage': np.random.uniform(0, 1, n_samples),
        'comment_ratio': np.random.uniform(0, 0.4, n_samples),

        # OOP metrics (3)
        'inheritance_depth': np.random.randint(0, 8, n_samples),
        'coupling': np.random.randint(0, 30, n_samples),
        'cohesion': np.random.uniform(0.3, 1.0, n_samples),

        # Security-related metrics (5)
        'num_sql_queries': np.random.randint(0, 20, n_samples),
        'num_file_operations': np.random.randint(0, 10, n_samples),
        'num_network_calls': np.random.randint(0, 15, n_samples),
        'input_validation_ratio': np.random.uniform(0, 1, n_samples),
        'uses_encryption': np.random.randint(0, 2, n_samples),

        # Pattern indicators (2)
        'num_annotations': np.random.randint(0, 30, n_samples),
        'dependency_injection_usage': np.random.uniform(0, 1, n_samples),
    }

    df = pd.DataFrame(data)
    
    print("\n" + "=" * 80)
    print("✅ FORCING GUARANTEED PATTERN SAMPLES (20 METRICS ONLY)")
    print("=" * 80)
    
    # ========== FORCE CREATE GUARANTEED SAMPLES ==========
    
    current_idx = 0
    forced_indices = set()
    
    # 1. FORCE SINGLETON SAMPLES (10% = 500 samples)
    print("\n1. Creating Singleton Design Pattern samples...")
    num_singleton = 500
    for i in range(num_singleton):
        idx = current_idx + i
        df.loc[idx, 'cohesion'] = np.random.uniform(0.90, 0.96)
        df.loc[idx, 'num_classes'] = 1
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(1, 4)
        df.loc[idx, 'num_methods'] = np.random.randint(1, 3)
        df.loc[idx, 'coupling'] = np.random.randint(0, 3)
        df.loc[idx, 'num_parameters'] = np.random.randint(0, 2)
        df.loc[idx, 'inheritance_depth'] = 0
        df.loc[idx, 'lines_of_code'] = np.random.randint(6, 15)
        forced_indices.add(idx)
    current_idx += num_singleton
    print(f"   ✓ Created {num_singleton} Singleton samples")
    
    # 2. FORCE FACTORY SAMPLES (20% = 1000 samples)
    print("2. Creating Factory Design Pattern samples...")
    num_factory = 1000
    for i in range(num_factory):
        idx = current_idx + i
        df.loc[idx, 'cohesion'] = np.random.uniform(0.82, 0.88)
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(3, 8)
        df.loc[idx, 'num_classes'] = 1
        df.loc[idx, 'num_methods'] = np.random.randint(1, 4)
        df.loc[idx, 'coupling'] = np.random.randint(1, 5)
        df.loc[idx, 'num_parameters'] = np.random.randint(0, 3)
        df.loc[idx, 'inheritance_depth'] = np.random.randint(0, 2)
        df.loc[idx, 'lines_of_code'] = np.random.randint(8, 20)
        forced_indices.add(idx)
    current_idx += num_factory
    print(f"   ✓ Created {num_factory} Factory samples")
    
    # 3. FORCE BUILDER SAMPLES (6% = 300 samples)
    print("3. Creating Builder Design Pattern samples...")
    num_builder = 300
    for i in range(num_builder):
        idx = current_idx + i
        df.loc[idx, 'cohesion'] = np.random.uniform(0.80, 0.95)
        df.loc[idx, 'num_parameters'] = np.random.randint(3, 8)
        df.loc[idx, 'num_methods'] = np.random.randint(2, 6)
        df.loc[idx, 'num_classes'] = 2
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(1, 3)
        df.loc[idx, 'lines_of_code'] = np.random.randint(8, 15)
        df.loc[idx, 'inheritance_depth'] = 0
        df.loc[idx, 'coupling'] = np.random.randint(1, 5)
        forced_indices.add(idx)
    current_idx += num_builder
    print(f"   ✓ Created {num_builder} Builder samples")
    
    # 4. FORCE ERROR HANDLING SAMPLES (4% = 200 samples)
    print("4. Creating Exception Handling samples...")
    num_error = 200
    for i in range(num_error):
        idx = current_idx + i
        df.loc[idx, 'num_annotations'] = np.random.randint(2, 5)
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(1, 3)
        df.loc[idx, 'num_methods'] = np.random.randint(2, 4)
        df.loc[idx, 'num_parameters'] = np.random.randint(2, 5)
        df.loc[idx, 'lines_of_code'] = np.random.randint(5, 12)
        df.loc[idx, 'num_classes'] = 1
        df.loc[idx, 'inheritance_depth'] = 0
        df.loc[idx, 'coupling'] = np.random.randint(1, 4)
        df.loc[idx, 'cohesion'] = np.random.uniform(0.75, 0.85)
        forced_indices.add(idx)
    current_idx += num_error
    print(f"   ✓ Created {num_error} Exception Handling samples")
    
    # 5. FORCE REACTIVE PROGRAMMING SAMPLES (4% = 200 samples)
    print("5. Creating Reactive Programming samples...")
    num_reactive = 200
    for i in range(num_reactive):
        idx = current_idx + i
        df.loc[idx, 'num_network_calls'] = np.random.randint(1, 5)
        df.loc[idx, 'num_annotations'] = np.random.randint(2, 6)
        df.loc[idx, 'num_methods'] = np.random.randint(1, 4)
        df.loc[idx, 'lines_of_code'] = np.random.randint(8, 40)
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(1, 4)
        df.loc[idx, 'cohesion'] = np.random.uniform(0.75, 0.90)
        df.loc[idx, 'coupling'] = np.random.randint(1, 6)
        df.loc[idx, 'num_parameters'] = np.random.randint(1, 4)
        df.loc[idx, 'dependency_injection_usage'] = np.random.uniform(0.4, 0.8)
        df.loc[idx, 'num_classes'] = 1
        df.loc[idx, 'inheritance_depth'] = 0
        df.loc[idx, 'num_sql_queries'] = 0
        df.loc[idx, 'test_coverage'] = np.random.uniform(0.6, 0.9)
        forced_indices.add(idx)
    current_idx += num_reactive
    print(f"   ✓ Created {num_reactive} Reactive Programming samples")
    
    # 6. FORCE CONDITIONAL FLOW SAMPLES (6% = 300 samples)
    print("6. Creating Conditional Control Flow samples...")
    num_conditional = 300
    for i in range(num_conditional):
        idx = current_idx + i
        df.loc[idx, 'cyclomatic_complexity'] = np.random.randint(4, 12)
        df.loc[idx, 'num_annotations'] = np.random.randint(0, 2)
        df.loc[idx, 'num_methods'] = np.random.randint(1, 3)
        df.loc[idx, 'cohesion'] = np.random.uniform(0.75, 0.90)
        df.loc[idx, 'lines_of_code'] = np.random.randint(8, 25)
        df.loc[idx, 'num_classes'] = 1
        df.loc[idx, 'inheritance_depth'] = 0
        df.loc[idx, 'coupling'] = np.random.randint(1, 4)
        forced_indices.add(idx)
    current_idx += num_conditional
    print(f"   ✓ Created {num_conditional} Conditional Control Flow samples")
    
    # 7. FORCE DEPENDENCY INJECTION SAMPLES (8% = 400 samples)
    print("7. Creating Dependency Injection samples...")
    num_di = 400
    for i in range(num_di):
        idx = current_idx + i
        df.loc[idx, 'num_annotations'] = np.random.randint(10, 20)
        df.loc[idx, 'dependency_injection_usage'] = np.random.uniform(0.6, 0.9)
        df.loc[idx, 'cohesion'] = np.random.uniform(0.70, 0.85)
        forced_indices.add(idx)
    current_idx += num_di
    print(f"   ✓ Created {num_di} Dependency Injection samples")
    
    # 8. FORCE SPRING MVC SAMPLES (6% = 300 samples)
    print("8. Creating Spring MVC samples...")
    num_mvc = 300
    for i in range(num_mvc):
        idx = current_idx + i
        df.loc[idx, 'num_annotations'] = np.random.randint(15, 25)
        df.loc[idx, 'num_methods'] = np.random.randint(5, 15)
        df.loc[idx, 'cohesion'] = np.random.uniform(0.65, 0.80)
        forced_indices.add(idx)
    current_idx += num_mvc
    print(f"   ✓ Created {num_mvc} Spring MVC samples")
    
    print(f"\n✅ Total forced samples: {len(forced_indices)}/{n_samples}")
    print("=" * 80)

    # Generate patterns based on metrics
    patterns = []
    for idx, row in df.iterrows():
        detected_patterns = []

        # === CREATIONAL PATTERNS (5) ===
        
        # Singleton
        is_singleton = (
            row['cohesion'] >= 0.89 and
            row['num_classes'] == 1 and
            row['cyclomatic_complexity'] <= 4 and
            row['num_methods'] <= 3 and
            row['coupling'] <= 3
        )
        if is_singleton:
            detected_patterns.append('Singleton Design Pattern')
        
        # Factory
        elif not is_singleton:
            is_factory = (
                row['cohesion'] >= 0.75 and
                row['cohesion'] <= 1.00 and
                row['cyclomatic_complexity'] >= 2 and
                row['cyclomatic_complexity'] <= 20 and
                row['num_classes'] <= 2 and
                row['num_methods'] >= 1 and
                row['num_methods'] <= 8 and
                row['num_parameters'] < 4
            )
            if is_factory:
                detected_patterns.append('factory_design_pattern')
        
        # Builder
        is_builder = (
            row['cohesion'] >= 0.80 and row['cohesion'] <= 0.95 and
            row['num_parameters'] >= 3 and row['num_parameters'] <= 8 and
            row['num_methods'] >= 2 and row['num_methods'] <= 6 and
            row['num_classes'] == 2 and
            row['cyclomatic_complexity'] <= 3 and
            row['inheritance_depth'] == 0 and
            row['lines_of_code'] >= 8 and row['lines_of_code'] <= 15
        )
        if is_builder and 'Singleton Design Pattern' not in detected_patterns and 'factory_design_pattern' not in detected_patterns:
            detected_patterns.append('builder_design_pattern')
        
        # Prototype
        if row['code_duplication'] >= 0.20 and row['num_classes'] >= 2:
            detected_patterns.append('prototype_design_pattern')
        
        # Abstract Factory
        if row['num_classes'] >= 5 and row['inheritance_depth'] >= 2 and row['coupling'] >= 12:
            detected_patterns.append('abstract_factory_design_pattern')

        # === STRUCTURAL PATTERNS (7) ===
        
        # Adapter
        if row['inheritance_depth'] >= 1 and row['num_methods'] <= 10 and row['coupling'] <= 12:
            detected_patterns.append('adapter_design_pattern')
        
        # Decorator
        if row['inheritance_depth'] >= 2 and row['num_methods'] >= 8 and row['coupling'] >= 10:
            detected_patterns.append('decorator_design_pattern')
        
        # Proxy
        if row['num_methods'] <= 10 and row['cyclomatic_complexity'] <= 10 and row['inheritance_depth'] >= 1:
            detected_patterns.append('proxy_design_pattern')
        
        # Composite
        is_composite = (
            row['nesting_depth'] >= 4 and
            row['num_classes'] >= 4 and
            row['cyclomatic_complexity'] >= 12
        )
        if is_composite and 'factory_design_pattern' not in detected_patterns:
            detected_patterns.append('composite_design_pattern')
        
        # Facade
        if row['num_methods'] >= 15 and row['coupling'] >= 20:
            detected_patterns.append('facade_design_pattern')
        
        # Bridge
        if row['inheritance_depth'] >= 2 and row['num_classes'] >= 4 and row['coupling'] >= 10:
            detected_patterns.append('bridge_design_pattern')
        
        # Flyweight
        if row['code_duplication'] < 0.1 and row['num_classes'] > 5:
            detected_patterns.append('flyweight_design_pattern')

        # === BEHAVIORAL PATTERNS (11) ===
        
        # Strategy
        is_strategy = (
            row['inheritance_depth'] >= 2 and
            row['cohesion'] > 0.7 and
            row['cyclomatic_complexity'] < 10 and
            row['num_classes'] >= 3
        )
        if is_strategy and 'factory_design_pattern' not in detected_patterns and 'Singleton Design Pattern' not in detected_patterns:
            detected_patterns.append('strategy_design_pattern')
        
        # Observer
        if row['num_methods'] > 15 and row['coupling'] > 15:
            detected_patterns.append('observer_design_pattern')
        
        # Command
        if row['num_methods'] > 10 and row['cyclomatic_complexity'] < 20:
            detected_patterns.append('command_design_pattern')
        
        # Template Method
        if row['inheritance_depth'] >= 1 and row['num_methods'] > 5:
            detected_patterns.append('template_method_design_pattern')
        
        # Iterator
        if row['num_methods'] > 8 and row['cohesion'] > 0.6:
            detected_patterns.append('iterator_design_pattern')
        
        # State
        if row['cyclomatic_complexity'] > 25 and row['num_methods'] > 10:
            detected_patterns.append('state_design_pattern')
        
        # Chain of Responsibility
        if row['inheritance_depth'] >= 2 and row['num_methods'] > 8:
            detected_patterns.append('chain_of_responsibility_design_pattern')
        
        # Mediator
        if row['coupling'] > 20 and row['num_classes'] > 5:
            detected_patterns.append('mediator_design_pattern')
        
        # Memento
        if row['num_methods'] > 12 and row['test_coverage'] > 0.6:
            detected_patterns.append('memento_design_pattern')
        
        # Visitor
        if row['inheritance_depth'] >= 3 and row['num_methods'] > 15:
            detected_patterns.append('visitor_design_pattern')
        
        # Interpreter
        if row['cyclomatic_complexity'] > 30 and row['nesting_depth'] > 5:
            detected_patterns.append('interpreter_design_pattern')

        # === SPRING FRAMEWORK PATTERNS (7) ===
        
        # Dependency Injection
        if row['num_annotations'] >= 10 and row['dependency_injection_usage'] >= 0.6:
            detected_patterns.append('dependency_injection')
        
        # Spring MVC
        if row['num_annotations'] >= 15:
            detected_patterns.append('spring_mvc_pattern')
        
        # RESTful API
        if row['num_network_calls'] > 5:
            detected_patterns.append('restful_api_pattern')
        
        # Repository
        if row['num_annotations'] > 7 and row['num_sql_queries'] > 2:
            detected_patterns.append('repository_pattern')
        
        # Service Layer
        if row['num_annotations'] > 9 and row['num_methods'] > 7:
            detected_patterns.append('service_layer_pattern')
        
        # DTO
        if row['num_parameters'] > 5 and row['num_methods'] < 15:
            detected_patterns.append('dto_pattern')
        
        # AOP
        if row['num_annotations'] > 12 and row['cyclomatic_complexity'] > 20:
            detected_patterns.append('aop_pattern')

        # === CORE JAVA CONCEPTS (6) ===
        
        # OOP Fundamentals
        if row['inheritance_depth'] > 0 and row['num_classes'] > 1:
            detected_patterns.append('oop_fundamentals')
        
        # Collections Framework
        if row['num_methods'] > 10 and row['lines_of_code'] > 100:
            detected_patterns.append('collections_framework')
        
        # Exception Handling
        is_exception = (
            row['num_annotations'] >= 2 and
            row['cyclomatic_complexity'] <= 3 and
            row['num_methods'] >= 2 and row['num_methods'] <= 4 and
            row['num_parameters'] >= 2 and row['num_parameters'] <= 5 and
            row['lines_of_code'] >= 5 and row['lines_of_code'] <= 12 and
            row['cohesion'] >= 0.75
        )
        if is_exception:
            detected_patterns.append('exception_handling')
        
        # Conditional Control Flow
        is_conditional = (
            row['cyclomatic_complexity'] >= 4 and row['cyclomatic_complexity'] <= 12 and
            row['num_annotations'] <= 2 and
            row['num_methods'] <= 3 and
            row['cohesion'] >= 0.75 and row['cohesion'] <= 0.90 and
            row['lines_of_code'] >= 8 and row['lines_of_code'] <= 25
        )
        # Check for reactive to avoid conflict
        is_reactive = (
            row['num_network_calls'] >= 1 and
            row['num_annotations'] >= 1 and
            row['num_methods'] >= 1 and
            row['lines_of_code'] >= 5 and row['lines_of_code'] <= 50 and
            row['cyclomatic_complexity'] <= 5 and
            row['cohesion'] >= 0.70 and
            row['coupling'] <= 8 and
            row['num_parameters'] <= 5 and
            row['dependency_injection_usage'] >= 0.3 and
            'factory_design_pattern' not in detected_patterns and
            'Singleton Design Pattern' not in detected_patterns and
            'exception_handling' not in detected_patterns
        )
        if is_conditional and not is_exception and not is_reactive:
            detected_patterns.append('conditional_control_flow')
        
        # Loops and Iteration
        if row['cyclomatic_complexity'] > 8 and row['lines_of_code'] > 50:
            detected_patterns.append('loops_and_iteration')
        
        # Basic Programming Constructs
        if row['lines_of_code'] < 100 and row['num_methods'] < 10:
            detected_patterns.append('basic_programming_constructs')

        # === MODERN JAVA FEATURES (2) ===
        
        # Optional & Null Safety
        if row['input_validation_ratio'] > 0.7:
            detected_patterns.append('optional_null_safety')
        
        # Functional Programming
        if row['num_methods'] > 20 and row['test_coverage'] > 0.7:
            detected_patterns.append('functional_programming')

        # === SPRING BOOT ECOSYSTEM (4) ===
        
        # Spring Boot Error Handling
        if row['cyclomatic_complexity'] > 25 and row['num_annotations'] > 8:
            detected_patterns.append('spring_boot_error_handling')
        
        # Reactive Programming
        if is_reactive:
            detected_patterns.append('reactive_programming')
        
        # Utility Libraries
        if row['num_methods'] > 15 and row['coupling'] < 5:
            detected_patterns.append('utility_libraries')
        
        # Lombok & JPA Annotations
        if row['num_annotations'] > 20:
            detected_patterns.append('lombok_jpa_annotations')

        # === WEB DEVELOPMENT (3) ===
        
        # Core Annotations & DI
        if row['num_annotations'] > 8 and row['dependency_injection_usage'] > 0.3:
            detected_patterns.append('core_annotations_di')
        
        # Web MVC Annotations
        if row['num_annotations'] > 12 and row['num_network_calls'] > 3:
            detected_patterns.append('web_mvc_annotations')
        
        # HTTP Request Processing
        if row['num_network_calls'] > 8 and row['input_validation_ratio'] > 0.4:
            detected_patterns.append('http_request_processing')

        # === API DOCUMENTATION (1) ===
        
        # OpenAPI Documentation
        if row['num_annotations'] > 18 and row['comment_ratio'] > 0.2:
            detected_patterns.append('openapi_documentation')

        # === DATABASE INTEGRATION (2) ===
        
        # Spring Data JPA
        if row['num_sql_queries'] > 5 and row['num_annotations'] > 10:
            detected_patterns.append('spring_data_jpa')
        
        # Batch Processing ETL
        if row['lines_of_code'] > 500 and row['num_methods'] > 20:
            detected_patterns.append('batch_processing_etl')

        patterns.append(','.join(detected_patterns) if detected_patterns else 'none')

    df['patterns'] = patterns

    # Generate vulnerability types
    vulnerabilities = []
    severities = []

    for idx, row in df.iterrows():
        if row['num_sql_queries'] > 5 and row['input_validation_ratio'] < 0.3:
            vuln = 'sql_injection'
            sev = 'HIGH' if row['input_validation_ratio'] < 0.1 else 'MEDIUM'
        elif row['num_file_operations'] > 3 and row['input_validation_ratio'] < 0.4:
            vuln = 'path_traversal'
            sev = 'HIGH' if row['input_validation_ratio'] < 0.2 else 'MEDIUM'
        elif row['uses_encryption'] == 0 and row['num_network_calls'] > 8:
            vuln = 'insecure_deserialization'
            sev = 'CRITICAL' if row['num_network_calls'] > 12 else 'HIGH'
        elif row['input_validation_ratio'] < 0.2 and row['num_network_calls'] > 3:
            vuln = 'xss'
            sev = 'HIGH'
        elif row['num_annotations'] > 20 and row['input_validation_ratio'] < 0.5:
            vuln = 'authentication_bypass'
            sev = 'CRITICAL' if row['input_validation_ratio'] < 0.3 else 'HIGH'
        elif row['num_file_operations'] > 5 and row['uses_encryption'] == 0:
            vuln = 'xxe'
            sev = 'MEDIUM'
        else:
            vuln = 'none'
            sev = 'LOW'

        vulnerabilities.append(vuln)
        severities.append(sev)

    df['vulnerability_type'] = vulnerabilities
    df['severity'] = severities

    return df


def save_comprehensive_training_data(output_path: str = 'comprehensive_training_data.csv'):
    """Generate and save comprehensive training data"""
    print("=" * 80)
    print("✅ FIXED: Generating training data with ONLY 20 metrics")
    print("Dataset: 5000 samples with 47+ Java/Spring theories")
    print("Matches api_server.py exactly - NO extra columns!")
    print("=" * 80)
    
    df = generate_comprehensive_training_data(n_samples=5000)

    df.to_csv(output_path, index=False)
    print(f"\n✅ Training data saved to {output_path}")
    print(f"📊 Dataset shape: {df.shape}")
    print(f"📊 Columns: {df.shape[1]} (20 metrics + 3 target columns)")
    
    # Verify column count
    expected_cols = 23  # 20 metrics + patterns + vulnerability_type + severity
    if df.shape[1] == expected_cols:
        print(f"✅ Column count correct: {df.shape[1]} columns")
    else:
        print(f"⚠️  Column count mismatch: {df.shape[1]} (expected {expected_cols})")
    
    # Count pattern occurrences
    print(f"\n" + "=" * 80)
    print("📚 PATTERN DISTRIBUTION VERIFICATION")
    print("=" * 80)
    
    all_patterns = []
    for pattern_str in df['patterns']:
        if pattern_str != 'none':
            all_patterns.extend(pattern_str.split(','))
    
    from collections import Counter
    pattern_counts = Counter(all_patterns)
    
    print("\n🎨 CREATIONAL DESIGN PATTERNS (5):")
    creational = ['Singleton Design Pattern', 'factory_design_pattern', 'builder_design_pattern', 'prototype_design_pattern', 'abstract_factory_design_pattern']
    for pattern in creational:
        count = pattern_counts.get(pattern, 0)
        status = "✅" if count >= 100 else "⚠️" if count > 0 else "❌"
        print(f"  {status} {pattern:40s}: {count:4d} samples")
    
    print(f"\n" + "=" * 80)
    print(f"✅ TOTAL UNIQUE THEORIES DETECTED: {len(pattern_counts)}")
    print(f"✅ Factory Design Pattern: {pattern_counts.get('factory_design_pattern', 0)} samples")
    print(f"✅ Singleton Design Pattern: {pattern_counts.get('Singleton Design Pattern', 0)} samples")
    print(f"✅ Builder Design Pattern: {pattern_counts.get('builder_design_pattern', 0)} samples")
    print("=" * 80)

    return df


if __name__ == "__main__":
    df = save_comprehensive_training_data()

    print("\n" + "=" * 80)
    print("✅ TRAINING DATA GENERATION COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run training pipeline: python train_pipeline.py")
    print("2. Start API server: python api_server.py")
    print("3. Test patterns: python test_pattern_detection.py")
    print("=" * 80)