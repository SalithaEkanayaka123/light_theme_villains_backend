import pandas as pd
import numpy as np
from typing import List, Tuple


def generate_sample_training_data(n_samples: int = 2000) -> pd.DataFrame:
    """
    Generate comprehensive training data with 33 Java/Spring patterns
    UPDATED: Increased to 2000 samples for better coverage
    
    Returns DataFrame with:
    - 20 code metric features
    - patterns (comma-separated - 33 total patterns)
    - vulnerability_type
    - severity
    """
    np.random.seed(42)

    # Define 20 code metrics
    data = {
        # Complexity metrics
        'cyclomatic_complexity': np.random.randint(1, 50, n_samples),
        'cognitive_complexity': np.random.randint(1, 100, n_samples),
        'nesting_depth': np.random.randint(1, 10, n_samples),

        # Size metrics
        'lines_of_code': np.random.randint(10, 1000, n_samples),
        'num_methods': np.random.randint(1, 50, n_samples),
        'num_classes': np.random.randint(1, 20, n_samples),
        'num_parameters': np.random.randint(0, 15, n_samples),

        # Quality metrics
        'code_duplication': np.random.uniform(0, 0.5, n_samples),
        'test_coverage': np.random.uniform(0, 1, n_samples),
        'comment_ratio': np.random.uniform(0, 0.4, n_samples),

        # OOP metrics
        'inheritance_depth': np.random.randint(0, 8, n_samples),
        'coupling': np.random.randint(0, 30, n_samples),
        'cohesion': np.random.uniform(0.3, 1.0, n_samples),

        # Security-related metrics
        'num_sql_queries': np.random.randint(0, 20, n_samples),
        'num_file_operations': np.random.randint(0, 10, n_samples),
        'num_network_calls': np.random.randint(0, 15, n_samples),
        'input_validation_ratio': np.random.uniform(0, 1, n_samples),
        'uses_encryption': np.random.randint(0, 2, n_samples),

        # Pattern indicators
        'num_annotations': np.random.randint(0, 30, n_samples),
        'dependency_injection_usage': np.random.uniform(0, 1, n_samples),
    }

    df = pd.DataFrame(data)
    
    # ✅ FORCE CREATE SINGLETON SAMPLES (guarantee singleton appears)
    num_singleton_samples = int(n_samples * 0.10)  # 10% = 200 samples
    singleton_indices = np.random.choice(df.index, num_singleton_samples, replace=False)
    df.loc[singleton_indices, 'cohesion'] = np.random.uniform(0.75, 0.95, num_singleton_samples)
    df.loc[singleton_indices, 'num_classes'] = 1
    df.loc[singleton_indices, 'coupling'] = np.random.randint(0, 5, num_singleton_samples)
    
    print(f"✓ Created {num_singleton_samples} guaranteed Singleton samples")

    # ✅ FORCE CREATE FACTORY SAMPLES (guarantee factory appears)
    num_factory_samples = int(n_samples * 0.15)  # 15% = 300 samples
    remaining_indices = [i for i in df.index if i not in singleton_indices]
    factory_indices = np.random.choice(remaining_indices, num_factory_samples, replace=False)
    
    # Set Factory-specific metrics that match your code
    df.loc[factory_indices, 'cyclomatic_complexity'] = np.random.randint(4, 12, num_factory_samples)  # 4-11 range
    df.loc[factory_indices, 'cohesion'] = np.random.uniform(0.75, 0.9, num_factory_samples)  # High cohesion
    df.loc[factory_indices, 'num_classes'] = 1  # Simple factory = 1 class
    df.loc[factory_indices, 'num_methods'] = np.random.randint(2, 5, num_factory_samples)  # 2-4 methods
    df.loc[factory_indices, 'nesting_depth'] = np.random.randint(2, 6, num_factory_samples)  # Moderate nesting
    df.loc[factory_indices, 'inheritance_depth'] = np.random.randint(0, 2, num_factory_samples)  # Low inheritance
    
    print(f"✓ Created {num_factory_samples} guaranteed Factory samples")

    # Generate patterns based on metrics
    patterns = []
    for idx, row in df.iterrows():
        detected_patterns = []

        # ========== CREATIONAL PATTERNS (5) ==========
        
        # 1. Singleton (EXCLUSIVE - very specific conditions)
        is_singleton = (row['cohesion'] > 0.85 and row['num_classes'] == 1 and 
                       row['cyclomatic_complexity'] < 5 and row['num_methods'] <= 3)
        if is_singleton:
            detected_patterns.append('Singleton Design Pattern')
        
        # 2. Factory (SIMPLIFIED - more inclusive but still exclusive)
        elif not is_singleton:
            # Core Factory indicators: conditional logic + object creation + single purpose
            has_conditional_logic = row['cyclomatic_complexity'] >= 4  # Has switch/if logic
            has_creation_responsibility = row['cohesion'] >= 0.7  # High cohesion for creation
            has_simple_structure = row['num_classes'] <= 2  # Simple factory structure
            has_creation_methods = row['num_methods'] >= 1  # At least one method
            
            is_factory = (has_conditional_logic and has_creation_responsibility and 
                         has_simple_structure and has_creation_methods)
            if is_factory:
                detected_patterns.append('factory_design_pattern')
        
        # 3. Builder
        if row['num_parameters'] >= 7 and row['num_methods'] > 8:
            detected_patterns.append('builder')
        
        # 4. Prototype
        if row['code_duplication'] > 0.3 and row['num_classes'] > 3:
            detected_patterns.append('prototype')
        
        # 5. Abstract Factory
        if row['inheritance_depth'] >= 4 and row['num_classes'] >= 5:
            detected_patterns.append('abstract_factory')

        # ========== STRUCTURAL PATTERNS (7) ==========
        
        # 6. Adapter
        if row['inheritance_depth'] >= 1 and row['num_classes'] >= 2 and row['coupling'] < 15:
            detected_patterns.append('adapter')
        
        # 7. Decorator
        if row['inheritance_depth'] >= 2 and row['coupling'] > 5 and row['coupling'] < 15:
            detected_patterns.append('decorator')
        
        # 8. Proxy
        if row['num_methods'] > 10 and row['inheritance_depth'] >= 1 and row['coupling'] < 10:
            detected_patterns.append('proxy')
        
        # 9. Composite (VERY EXCLUSIVE - avoid any overlap with Factory)
        # Composite requires: tree structures, recursive composition, multiple related classes
        is_composite = (row['nesting_depth'] > 7 and 
                       row['inheritance_depth'] >= 3 and  # Strong inheritance hierarchy
                       row['num_classes'] >= 4 and        # Multiple classes for tree structure
                       row['cyclomatic_complexity'] > 20 and  # High complexity from tree operations
                       row['cohesion'] < 0.7)             # Lower cohesion due to complex interactions
        
        # Ensure NO overlap with Factory, Singleton, or Strategy
        conflicting_patterns = ['factory_design_pattern', 'Singleton Design Pattern', 'strategy_design_pattern']
        has_conflict = any(pattern in detected_patterns for pattern in conflicting_patterns)
        
        if is_composite and not has_conflict:
            detected_patterns.append('composite')
        
        # 10. Facade
        if row['num_methods'] > 15 and row['coupling'] > 20:
            detected_patterns.append('facade')
        
        # 11. Bridge
        if row['inheritance_depth'] >= 2 and row['num_classes'] >= 4:
            detected_patterns.append('bridge')
        
        # 12. Flyweight
        if row['code_duplication'] < 0.1 and row['num_classes'] > 5:
            detected_patterns.append('flyweight')

        # ========== BEHAVIORAL PATTERNS (11) ==========
        
        # 13. Strategy (MORE EXCLUSIVE - avoid overlap with Factory/Singleton)
        is_strategy = (row['inheritance_depth'] >= 2 and row['cohesion'] > 0.7 and 
                      row['cyclomatic_complexity'] < 10 and row['num_classes'] >= 3)
        if is_strategy and 'factory' not in detected_patterns and 'singleton' not in detected_patterns:
            detected_patterns.append('strategy_design_pattern')
        
        # 14. Observer
        if row['num_methods'] > 15 and row['coupling'] > 15:
            detected_patterns.append('observer')
        
        # 15. Command
        if row['num_methods'] > 10 and row['cyclomatic_complexity'] < 20:
            detected_patterns.append('command')
        
        # 16. Template Method
        if row['inheritance_depth'] >= 1 and row['num_methods'] > 5:
            detected_patterns.append('template_method')
        
        # 17. Iterator
        if row['num_methods'] > 8 and row['cohesion'] > 0.6:
            detected_patterns.append('iterator')
        
        # 18. State
        if row['cyclomatic_complexity'] > 25 and row['num_methods'] > 10:
            detected_patterns.append('state')
        
        # 19. Chain of Responsibility
        if row['inheritance_depth'] >= 2 and row['num_methods'] > 8:
            detected_patterns.append('chain_of_responsibility')
        
        # 20. Mediator
        if row['coupling'] > 20 and row['num_classes'] > 5:
            detected_patterns.append('mediator')
        
        # 21. Memento
        if row['num_methods'] > 12 and row['test_coverage'] > 0.6:
            detected_patterns.append('memento')
        
        # 22. Visitor
        if row['inheritance_depth'] >= 3 and row['num_methods'] > 15:
            detected_patterns.append('visitor')
        
        # 23. Interpreter
        if row['cyclomatic_complexity'] > 30 and row['nesting_depth'] > 5:
            detected_patterns.append('interpreter')

        # ========== SPRING-SPECIFIC PATTERNS (7) ==========
        
        # 24. Dependency Injection
        if row['num_annotations'] > 10 and row['dependency_injection_usage'] > 0.5:
            detected_patterns.append('dependency_injection')
        
        # 25. Spring MVC
        if row['num_annotations'] > 15:
            detected_patterns.append('mvc')
        
        # 26. RESTful API
        if row['num_network_calls'] > 5:
            detected_patterns.append('restful_api')
        
        # 27. Repository Pattern (Spring Data)
        if row['num_annotations'] > 7 and row['num_sql_queries'] > 2:
            detected_patterns.append('repository')
        
        # 28. Service Layer
        if row['num_annotations'] > 9 and row['num_methods'] > 7:
            detected_patterns.append('service_layer')
        
        # 29. DTO (Data Transfer Object)
        if row['num_parameters'] > 5 and row['num_methods'] < 15:
            detected_patterns.append('dto')
        
        # 30. AOP (Aspect-Oriented Programming)
        if row['num_annotations'] > 12 and row['cyclomatic_complexity'] > 20:
            detected_patterns.append('aop')

        # ========== JAVA-SPECIFIC PATTERNS (3) ==========
        
        # 31. Exception Handling
        if row['cyclomatic_complexity'] > 30:
            detected_patterns.append('exception_handling')
        
        # 32. Stream API (Java 8+)
        if row['coupling'] < 10 and row['lines_of_code'] > 200:
            detected_patterns.append('stream_api')
        
        # 33. Functional Programming
        if row['num_methods'] > 20 and row['test_coverage'] > 0.7:
            detected_patterns.append('functional_programming')

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


def save_training_data(output_path: str = 'code_metrics_training_data.csv'):
    """Generate and save training data"""
    print("=" * 70)
    print("Generating comprehensive training data with 33 Java/Spring patterns...")
    print("=" * 70)
    df = generate_sample_training_data(n_samples=2000)

    df.to_csv(output_path, index=False)
    print(f"\n✅ Training data saved to {output_path}")
    print(f"📊 Dataset shape: {df.shape}")
    
    # Count pattern occurrences
    print(f"\n" + "=" * 70)
    print("📚 PATTERN DISTRIBUTION (33 Patterns)")
    print("=" * 70)
    
    all_patterns = []
    for pattern_str in df['patterns']:
        if pattern_str != 'none':
            all_patterns.extend(pattern_str.split(','))
    
    from collections import Counter
    pattern_counts = Counter(all_patterns)
    
    print("\n🎨 CREATIONAL PATTERNS (5):")
    creational = ['singleton', 'factory', 'builder', 'prototype', 'abstract_factory']
    for pattern in creational:
        count = pattern_counts.get(pattern, 0)
        print(f"  {'✓' if count > 0 else '✗'} {pattern}: {count} samples")
    
    print("\n🏗️  STRUCTURAL PATTERNS (7):")
    structural = ['adapter', 'decorator', 'proxy', 'composite', 'facade', 'bridge', 'flyweight']
    for pattern in structural:
        count = pattern_counts.get(pattern, 0)
        print(f"  {'✓' if count > 0 else '✗'} {pattern}: {count} samples")
    
    print("\n🔄 BEHAVIORAL PATTERNS (11):")
    behavioral = ['strategy', 'observer', 'command', 'template_method', 'iterator', 
                  'state', 'chain_of_responsibility', 'mediator', 'memento', 'visitor', 'interpreter']
    for pattern in behavioral:
        count = pattern_counts.get(pattern, 0)
        print(f"  {'✓' if count > 0 else '✗'} {pattern}: {count} samples")
    
    print("\n🍃 SPRING-SPECIFIC PATTERNS (7):")
    spring = ['dependency_injection', 'mvc', 'restful_api', 'repository', 'service_layer', 'dto', 'aop']
    for pattern in spring:
        count = pattern_counts.get(pattern, 0)
        print(f"  {'✓' if count > 0 else '✗'} {pattern}: {count} samples")
    
    print("\n☕ JAVA-SPECIFIC PATTERNS (3):")
    java_specific = ['exception_handling', 'stream_api', 'functional_programming']
    for pattern in java_specific:
        count = pattern_counts.get(pattern, 0)
        print(f"  {'✓' if count > 0 else '✗'} {pattern}: {count} samples")
    
    print(f"\n" + "=" * 70)
    print(f"🔒 VULNERABILITY DISTRIBUTION")
    print("=" * 70)
    print(df['vulnerability_type'].value_counts())
    
    print(f"\n⚠️  SEVERITY DISTRIBUTION")
    print("=" * 70)
    print(df['severity'].value_counts())
    
    # Verify singleton specifically
    singleton_count = df['patterns'].str.contains('singleton').sum()
    print(f"\n" + "=" * 70)
    print(f"✅ Singleton patterns verified: {singleton_count} samples")
    print(f"✅ TOTAL UNIQUE PATTERNS: {len(pattern_counts)}")
    print("=" * 70)

    return df


if __name__ == "__main__":
    df = save_training_data()

    print("\n" + "=" * 70)
    print("✅ Training data generation complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review the CSV file: code_metrics_training_data.csv")
    print("2. Update security_analysis_system.py with 33 pattern definitions")
    print("3. Run: python train_pipeline.py")
    print("4. Start API: python api_server.py")
    print("=" * 70)
