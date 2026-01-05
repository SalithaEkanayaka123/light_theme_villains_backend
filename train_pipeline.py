"""
Complete Training Pipeline
Generates data, trains models, and validates the system
"""

import pandas as pd
import numpy as np
from generate_training_data import generate_sample_training_data, save_training_data
from security_analysis_system import (
    train_models_from_csv, 
    Agent1_TheoryDetector, 
    Agent2_SecurityAnalyzer,
    Agent3_OutputAggregator
)
import os

def complete_training_pipeline():
    """
    Complete pipeline:
    1. Generate training data (or load existing)
    2. Train Agent 1 (Theory Detection)
    3. Train Agent 2 (Security Analysis)
    4. Validate models
    5. Run test predictions
    """
    
    print("=" * 70)
    print("JAVA CODE SECURITY ANALYSIS - TRAINING PIPELINE")
    print("=" * 70)
    
    # Step 1: Generate or load training data
    print("\n[Step 1] Preparing Training Data...")
    
    # Use comprehensive training data (5000 samples, 47+ theories) if available
    if os.path.exists('comprehensive_training_data.csv'):
        csv_path = 'comprehensive_training_data.csv'
        print(f"Using comprehensive training data with 47+ Java theories")
    else:
        csv_path = 'code_metrics_training_data.csv'
        print(f"Using basic training data")
    
    if os.path.exists(csv_path):
        print(f"Loading existing training data from {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print("Generating new training data...")
        df = save_training_data(csv_path)
    
    print(f"✓ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
    
    # Step 2 & 3: Train both agents
    print("\n[Step 2 & 3] Training Agent Models...")
    agent1, agent2 = train_models_from_csv(csv_path)
    
    print("\n✓ Both agents trained successfully!")
    
    # Step 4: Validation
    print("\n[Step 4] Validating Models...")
    
    # Load test sample
    test_sample = df.sample(5)
    feature_columns = [col for col in df.columns 
                      if col not in ['patterns', 'vulnerability_type', 'severity']]
    X_test = test_sample[feature_columns]
    
    # Agent 1 predictions
    print("\n--- Agent 1: Theory Detection ---")
    theory_predictions = agent1.predict(X_test)
    for i, pred in enumerate(theory_predictions):
        print(f"\nSample {i+1}:")
        if pred:
            for pattern in pred[:3]:  # Show top 3
                print(f"  • {pattern['pattern']}: {pattern['confidence']:.2f}")
        else:
            print("  No patterns detected")
    
    # Agent 2 predictions
    print("\n--- Agent 2: Security Analysis ---")
    security_predictions = agent2.predict(X_test)
    for i, pred in enumerate(security_predictions):
        print(f"\nSample {i+1}:")
        print(f"  Vulnerability: {pred['vulnerability']}")
        print(f"  Severity: {pred['severity']}")
        print(f"  Confidence: {pred['confidence']:.2f}")
    
    # Step 5: Test Agent 3 aggregation
    print("\n[Step 5] Testing Agent 3 Aggregation...")
    
    # ✅ FIXED: Properly format inputs for Agent3
    # theory_predictions[0] is already a list of dicts
    # security_predictions[0] is a dict, so we wrap it in a list
    final_output = Agent3_OutputAggregator.aggregate(
        theory_results=theory_predictions[0] if theory_predictions[0] else [],
        security_results=[security_predictions[0]],  # ✅ Wrap in list
        code_snippet="Test Java code snippet"
    )
    
    print("\n--- Agent 3: Aggregated Output ---")
    print(f"Patterns detected: {final_output['theory_analysis']['patterns_detected']}")
    print(f"Vulnerabilities found: {final_output['security_analysis']['vulnerabilities_found']}")
    print(f"Risk level: {final_output['security_analysis']['risk_level']}")
    print(f"Recommendations: {len(final_output['recommendations'])}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)
    print("\nModel files created:")
    print("  ✓ agent1_theory_detector.pkl")
    print("  ✓ agent2_security_analyzer.pkl")
    print(f"  ✓ {csv_path}")
    print("\nNext steps:")
    print("  1. Start API server: python api_server.py")
    print("  2. Send Java code to POST /analyze endpoint")
    print("  3. Integrate with your frontend")
    print("=" * 70)


if __name__ == "__main__":
    complete_training_pipeline()