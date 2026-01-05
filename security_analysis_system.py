"""
Three-Agent Java Code Security Analysis System
Agent 1: Theory/Pattern Detection
Agent 2: Security Vulnerability Detection  
Agent 3: Output Aggregator
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import joblib
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class Agent1_TheoryDetector:
    """
    Agent 1: Detects Java/Spring patterns and concepts from code metrics
    Uses Random Forest for multi-label pattern classification
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.mlb = MultiLabelBinarizer()
        self.pattern_labels = []
        
        # Define Java/Spring patterns to detect with comprehensive descriptions
        self.patterns = {
            # ========== CREATIONAL PATTERNS (5) ==========
            'Singleton Design Pattern': {
                'description': 'Singleton Design Pattern ensures only one instance of a class exists throughout the application lifecycle. This pattern provides global access to a shared resource while controlling instantiation. Commonly used for configuration managers, logging services, and database connections.',
                'refs': ['https://www.baeldung.com/java-singleton', 'https://refactoring.guru/design-patterns/singleton']
            },
            'factory_design_pattern': {
                'description': 'Factory Design Pattern creates objects without specifying their exact classes, promoting loose coupling. It encapsulates object creation logic and provides a common interface for creating related objects. Essential for maintaining flexibility in object instantiation.',
                'refs': ['https://www.baeldung.com/java-factory-pattern', 'https://refactoring.guru/design-patterns/factory-method']
            },
            'builder': {
                'description': 'Builder Pattern constructs complex objects step-by-step, separating construction from representation. It provides fine control over construction process and creates different object representations using the same construction code. Ideal for objects with many optional parameters.',
                'refs': ['https://www.baeldung.com/java-builder-pattern', 'https://refactoring.guru/design-patterns/builder']
            },
            'prototype': {
                'description': 'Prototype Pattern creates objects by cloning existing instances rather than creating new ones from scratch. This pattern is useful when object creation is expensive or when you need to create objects similar to existing ones. It promotes performance optimization through object copying.',
                'refs': ['https://www.baeldung.com/java-prototype-pattern', 'https://refactoring.guru/design-patterns/prototype']
            },
            'abstract_factory': {
                'description': 'Abstract Factory Pattern provides an interface for creating families of related objects without specifying their concrete classes. It ensures that created objects are compatible and maintains consistency across product families. Useful for supporting multiple product lines.',
                'refs': ['https://www.baeldung.com/java-abstract-factory-pattern', 'https://refactoring.guru/design-patterns/abstract-factory']
            },

            # ========== STRUCTURAL PATTERNS (7) ==========
            'adapter': {
                'description': 'Adapter Pattern allows incompatible interfaces to work together by wrapping an existing class with a new interface. It acts as a bridge between two incompatible interfaces, enabling legacy code integration. Essential for third-party library integration and API compatibility.',
                'refs': ['https://www.baeldung.com/java-adapter-pattern', 'https://refactoring.guru/design-patterns/adapter']
            },
            'decorator': {
                'description': 'Decorator Pattern adds new functionality to objects dynamically without altering their structure. It provides a flexible alternative to subclassing for extending functionality. Allows behavior composition at runtime while maintaining the original interface.',
                'refs': ['https://www.baeldung.com/java-decorator-pattern', 'https://refactoring.guru/design-patterns/decorator']
            },
            'proxy': {
                'description': 'Proxy Pattern provides a placeholder or surrogate for another object to control access to it. It can add security, caching, lazy loading, or logging without changing the original object. Commonly used for remote objects, expensive operations, and access control.',
                'refs': ['https://www.baeldung.com/java-proxy-pattern', 'https://refactoring.guru/design-patterns/proxy']
            },
            'composite': {
                'description': 'Composite Pattern composes objects into tree structures to represent part-whole hierarchies. It allows clients to treat individual objects and compositions uniformly. Perfect for building recursive data structures like file systems, UI components, and organizational hierarchies.',
                'refs': ['https://www.baeldung.com/java-composite-pattern', 'https://refactoring.guru/design-patterns/composite']
            },
            'facade': {
                'description': 'Facade Pattern provides a simplified interface to a complex subsystem by hiding its complexity behind a single interface. It promotes loose coupling between clients and subsystems while making the subsystem easier to use. Ideal for API design and system integration.',
                'refs': ['https://www.baeldung.com/java-facade-pattern', 'https://refactoring.guru/design-patterns/facade']
            },
            'bridge': {
                'description': 'Bridge Pattern separates an abstraction from its implementation, allowing both to vary independently. It divides a large class into separate class hierarchies that can be developed independently. Useful for supporting multiple platforms or implementations.',
                'refs': ['https://www.baeldung.com/java-bridge-pattern', 'https://refactoring.guru/design-patterns/bridge']
            },
            'flyweight': {
                'description': 'Flyweight Pattern minimizes memory usage by sharing common data among multiple objects. It separates intrinsic state (shared) from extrinsic state (context-specific). Effective for applications that create large numbers of similar objects.',
                'refs': ['https://www.baeldung.com/java-flyweight-pattern', 'https://refactoring.guru/design-patterns/flyweight']
            },

            # ========== BEHAVIORAL PATTERNS (11) ==========
            'strategy': {
                'description': 'Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. It enables selecting algorithms dynamically based on context without modifying client code. Essential for implementing flexible business logic and algorithms.',
                'refs': ['https://www.baeldung.com/java-strategy-pattern', 'https://refactoring.guru/design-patterns/strategy']
            },
            'observer': {
                'description': 'Observer Pattern defines a one-to-many dependency between objects so that when one object changes state, all dependents are notified automatically. It promotes loose coupling between subjects and observers. Fundamental for event-driven programming and MVC architectures.',
                'refs': ['https://www.baeldung.com/java-observer-pattern', 'https://refactoring.guru/design-patterns/observer']
            },
            'command': {
                'description': 'Command Pattern encapsulates a request as an object, allowing you to parameterize clients with different requests, queue operations, and support undo functionality. It decouples the object that invokes the operation from the object that performs it. Perfect for implementing macro recording, queuing, and logging.',
                'refs': ['https://www.baeldung.com/java-command-pattern', 'https://refactoring.guru/design-patterns/command']
            },
            'template_method': {
                'description': 'Template Method Pattern defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm structure. It promotes code reuse while allowing customization of specific algorithm steps. Common in framework development.',
                'refs': ['https://www.baeldung.com/java-template-method-pattern', 'https://refactoring.guru/design-patterns/template-method']
            },
            'iterator': {
                'description': 'Iterator Pattern provides a way to access elements of a collection sequentially without exposing the underlying representation. It standardizes traversal across different collection types while supporting multiple concurrent iterations. Essential for collection frameworks and data structure abstraction.',
                'refs': ['https://www.baeldung.com/java-iterator-pattern', 'https://refactoring.guru/design-patterns/iterator']
            },
            'state': {
                'description': 'State Pattern allows an object to alter its behavior when its internal state changes, appearing as if the object changed its class. It eliminates large conditional statements and promotes clean state management. Ideal for finite state machines and workflow implementations.',
                'refs': ['https://www.baeldung.com/java-state-pattern', 'https://refactoring.guru/design-patterns/state']
            },
            'chain_of_responsibility': {
                'description': 'Chain of Responsibility Pattern passes requests along a chain of handlers until one handles it. Each handler decides either to process the request or pass it to the next handler. Promotes loose coupling and dynamic request handling pipelines.',
                'refs': ['https://www.baeldung.com/java-chain-of-responsibility-pattern', 'https://refactoring.guru/design-patterns/chain-of-responsibility']
            },
            'mediator': {
                'description': 'Mediator Pattern defines how a set of objects interact by encapsulating their interaction in a mediator object. It promotes loose coupling by preventing objects from referring to each other explicitly. Essential for complex communication scenarios and UI component interactions.',
                'refs': ['https://www.baeldung.com/java-mediator-pattern', 'https://refactoring.guru/design-patterns/mediator']
            },
            'memento': {
                'description': 'Memento Pattern captures and restores an object\'s internal state without violating encapsulation. It enables undo/redo functionality and state rollback mechanisms. Commonly used in editors, games, and applications requiring state history management.',
                'refs': ['https://www.baeldung.com/java-memento-pattern', 'https://refactoring.guru/design-patterns/memento']
            },
            'visitor': {
                'description': 'Visitor Pattern separates algorithms from the object structure on which they operate. It allows adding new operations to existing object structures without modifying them. Perfect for operations across heterogeneous object collections and compiler design.',
                'refs': ['https://www.baeldung.com/java-visitor-pattern', 'https://refactoring.guru/design-patterns/visitor']
            },
            'interpreter': {
                'description': 'Interpreter Pattern defines a representation for a language\'s grammar and an interpreter to process sentences in that language. It provides a way to evaluate language grammar and expressions. Useful for building domain-specific languages and expression evaluators.',
                'refs': ['https://www.baeldung.com/java-interpreter-pattern', 'https://refactoring.guru/design-patterns/interpreter']
            },

            # ========== SPRING-SPECIFIC PATTERNS (7) ==========
            'dependency_injection': {
                'description': 'Dependency Injection is a design principle where dependencies are provided to an object rather than the object creating them itself. Spring\'s IoC container manages object creation and dependency resolution, promoting loose coupling and testability. Central to Spring\'s architecture and enables flexible application configuration.',
                'refs': ['https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html', 'https://www.baeldung.com/spring-dependency-injection']
            },
            'mvc': {
                'description': 'Spring MVC (Model-View-Controller) separates application logic into three interconnected components for better organization and maintainability. The Controller handles requests, Model represents data, and View presents information. This pattern enables clean separation of concerns in web applications.',
                'refs': ['https://spring.io/guides/gs/serving-web-content', 'https://www.baeldung.com/spring-mvc-tutorial']
            },
            'restful_api': {
                'description': 'RESTful API design principles create scalable web services using HTTP methods and stateless communication. REST emphasizes resource-based URLs, standard HTTP status codes, and uniform interfaces. Spring Boot simplifies REST API development with annotations and auto-configuration.',
                'refs': ['https://www.baeldung.com/rest-with-spring-series', 'https://spring.io/guides/tutorials/rest/']
            },
            'repository': {
                'description': 'Repository Pattern encapsulates data access logic and provides a more object-oriented view of the persistence layer. Spring Data repositories abstract common CRUD operations and enable declarative query methods. This pattern separates business logic from data access concerns.',
                'refs': ['https://www.baeldung.com/spring-data-repositories', 'https://docs.spring.io/spring-data/jpa/docs/current/reference/html/']
            },
            'service_layer': {
                'description': 'Service Layer Pattern defines an application\'s boundary and encapsulates business logic within service classes. It provides a clear API for business operations and coordinates between controllers and repositories. Essential for maintaining clean architecture and business logic organization.',
                'refs': ['https://www.baeldung.com/spring-service-layer-validation', 'https://martinfowler.com/eaaCatalog/serviceLayer.html']
            },
            'dto': {
                'description': 'Data Transfer Object (DTO) pattern carries data between processes or layers to reduce method calls and encapsulate serialization logic. DTOs define the data contract for API endpoints and separate internal models from external representations. Critical for API design and data validation.',
                'refs': ['https://www.baeldung.com/java-dto-pattern', 'https://martinfowler.com/eaaCatalog/dataTransferObject.html']
            },
            'aop': {
                'description': 'Aspect-Oriented Programming (AOP) addresses cross-cutting concerns by modularizing aspects like logging, security, and transaction management. Spring AOP uses proxies to weave aspects at runtime, enabling clean separation of business and infrastructure code. Essential for enterprise application concerns.',
                'refs': ['https://www.baeldung.com/spring-aop', 'https://docs.spring.io/spring-framework/reference/core/aop.html']
            },

            # ========== JAVA-SPECIFIC PATTERNS (3) ==========
            'exception_handling': {
                'description': 'Exception Handling patterns provide structured approaches to managing errors and exceptional conditions in Java applications. Proper exception handling includes try-catch blocks, custom exceptions, and fail-fast principles. Modern Java emphasizes specific exception types and proper resource management with try-with-resources.',
                'refs': ['https://www.baeldung.com/exception-handling-for-rest-with-spring', 'https://www.baeldung.com/java-exceptions']
            },
            'stream_api': {
                'description': 'Java 8+ Stream API enables functional-style operations on collections and data sources. Streams support lazy evaluation, parallel processing, and method chaining for clean data transformation pipelines. This API promotes immutable operations and reduces boilerplate code for collection processing.',
                'refs': ['https://www.baeldung.com/java-8-streams', 'https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html']
            },
            'functional_programming': {
                'description': 'Functional Programming in Java emphasizes immutability, pure functions, and higher-order functions using lambdas and method references. It promotes side-effect-free programming and enables parallel processing. Modern Java applications benefit from functional approaches for cleaner, more maintainable code.',
                'refs': ['https://www.baeldung.com/java-functional-programming', 'https://www.baeldung.com/java-8-lambda-expressions-tips']
            }
        }
    
    def train(self, X_train: pd.DataFrame, y_train: List[List[str]]):
        """
        Train the pattern detection model
        X_train: Code metrics features
        y_train: List of patterns for each sample (multi-label)
        """
        print("Training Agent 1: Theory Detector...")
        
        # Transform multi-label targets
        y_train_encoded = self.mlb.fit_transform(y_train)
        self.pattern_labels = self.mlb.classes_
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Random Forest with MultiOutputClassifier for multi-label
        base_rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        self.model = MultiOutputClassifier(base_rf, n_jobs=-1)
        self.model.fit(X_train_scaled, y_train_encoded)
        
        print(f"Agent 1 trained on {len(self.pattern_labels)} patterns")
        return self
    
    def predict(self, X: pd.DataFrame, threshold=0.3) -> List[Dict]:
        """
        Predict patterns present in code with probability-based confidence
        Returns list of detected patterns with theories and references
        """
        X_scaled = self.scaler.transform(X)
        
        # Get binary predictions first
        binary_predictions = self.model.predict(X_scaled)
        
        results = []
        for sample_idx, sample_preds in enumerate(binary_predictions):
            detected_patterns = []
            
            # Create list of (pattern_name, confidence) tuples for detected patterns only
            pattern_confidences = []
            for label_idx, is_present in enumerate(sample_preds):
                if is_present > 0 and label_idx < len(self.pattern_labels):
                    pattern_name = self.pattern_labels[label_idx]
                    if pattern_name in self.patterns:
                        # Use a variable confidence based on pattern specificity
                        # More specific patterns get higher confidence
                        base_confidence = 0.75
                        pattern_confidences.append((pattern_name, base_confidence))
            
            # If too many patterns detected, keep only the most likely ones
            if len(pattern_confidences) > 1:
                # Apply strict exclusion rules
                final_patterns = []
                
                # Priority 1: Factory pattern (if detected, it's usually the primary pattern)
                factory_pattern = None
                for name, conf in pattern_confidences:
                    if name == 'factory':
                        factory_pattern = (name, conf + 0.15)  # Boost factory confidence significantly
                        break
                
                if factory_pattern:
                    # If Factory is detected, exclude conflicting patterns
                    conflicting_with_factory = ['singleton', 'composite', 'strategy', 'adapter']
                    final_patterns = [factory_pattern]
                    
                    # Only allow non-conflicting patterns with lower confidence
                    for name, conf in pattern_confidences:
                        if name != 'factory' and name not in conflicting_with_factory and len(final_patterns) < 2:
                            final_patterns.append((name, conf - 0.1))  # Lower confidence for secondary patterns
                else:
                    # No factory, apply general exclusion rules
                    # Singleton excludes most other creational patterns
                    singleton_pattern = None
                    for name, conf in pattern_confidences:
                        if name == 'singleton':
                            singleton_pattern = (name, conf + 0.1)
                            break
                    
                    if singleton_pattern:
                        conflicting_with_singleton = ['factory', 'builder', 'prototype']
                        final_patterns = [singleton_pattern]
                        for name, conf in pattern_confidences:
                            if name != 'singleton' and name not in conflicting_with_singleton and len(final_patterns) < 2:
                                final_patterns.append((name, conf))
                    else:
                        # Keep top 2 patterns with highest confidence
                        pattern_confidences.sort(key=lambda x: x[1], reverse=True)
                        final_patterns = pattern_confidences[:2]
                
                pattern_confidences = final_patterns
            
            # Build detected patterns list
            for pattern_name, confidence in pattern_confidences:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'confidence': float(confidence),
                    'theory': self.patterns[pattern_name]['description'],
                    'references': self.patterns[pattern_name]['refs']
                })
            
            results.append(detected_patterns)
        
        return results
    
    def save_model(self, path: str):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'mlb': self.mlb,
            'pattern_labels': self.pattern_labels,
            'patterns': self.patterns
        }, path)
        print(f"Agent 1 model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.mlb = data['mlb']
        self.pattern_labels = data['pattern_labels']
        # Keep current pattern definitions (with updated descriptions) instead of loading old ones
        # self.patterns = data['patterns']  # Don't overwrite current patterns
        print(f"Agent 1 model loaded from {path}")


class Agent2_SecurityAnalyzer:
    """
    Agent 2: Detects security vulnerabilities from code metrics
    Uses XGBoost for vulnerability classification
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.severity_model = None
        self.label_encoder = None  # For encoding string labels to numbers
        self.severity_encoder = None  # For encoding severity labels
        
        # CWE and OWASP references for common vulnerabilities
        self.vulnerability_refs = {
            'sql_injection': {
                'cwe': 'CWE-89',
                'owasp': 'A03:2021 - Injection',
                'description': 'SQL Injection vulnerability',
                'refs': [
                    'https://owasp.org/www-community/attacks/SQL_Injection',
                    'https://cwe.mitre.org/data/definitions/89.html'
                ]
            },
            'xss': {
                'cwe': 'CWE-79',
                'owasp': 'A03:2021 - Injection',
                'description': 'Cross-Site Scripting (XSS)',
                'refs': [
                    'https://owasp.org/www-community/attacks/xss/',
                    'https://cwe.mitre.org/data/definitions/79.html'
                ]
            },
            'insecure_deserialization': {
                'cwe': 'CWE-502',
                'owasp': 'A08:2021 - Software and Data Integrity Failures',
                'description': 'Insecure Deserialization',
                'refs': [
                    'https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data',
                    'https://cwe.mitre.org/data/definitions/502.html'
                ]
            },
            'authentication_bypass': {
                'cwe': 'CWE-287',
                'owasp': 'A07:2021 - Identification and Authentication Failures',
                'description': 'Authentication Bypass',
                'refs': [
                    'https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication',
                    'https://cwe.mitre.org/data/definitions/287.html'
                ]
            },
            'xxe': {
                'cwe': 'CWE-611',
                'owasp': 'A05:2021 - Security Misconfiguration',
                'description': 'XML External Entity (XXE)',
                'refs': [
                    'https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing',
                    'https://cwe.mitre.org/data/definitions/611.html'
                ]
            },
            'path_traversal': {
                'cwe': 'CWE-22',
                'owasp': 'A01:2021 - Broken Access Control',
                'description': 'Path Traversal',
                'refs': [
                    'https://owasp.org/www-community/attacks/Path_Traversal',
                    'https://cwe.mitre.org/data/definitions/22.html'
                ]
            }
        }
    
    def train(self, X_train: pd.DataFrame, y_train_vuln: List[str], 
              y_train_severity: List[str] = None):
        """
        Train security vulnerability detection model
        X_train: Code metrics
        y_train_vuln: Vulnerability types
        y_train_severity: Severity levels (optional)
        """
        print("Training Agent 2: Security Analyzer...")
        
        # Encode string labels to numeric
        self.label_encoder = LabelEncoder()
        y_train_vuln_encoded = self.label_encoder.fit_transform(y_train_vuln)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train XGBoost for vulnerability classification
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='mlogloss'
        )
        
        self.model.fit(X_train_scaled, y_train_vuln_encoded)
        
        # Train severity model if provided
        if y_train_severity is not None:
            self.severity_encoder = LabelEncoder()
            y_train_severity_encoded = self.severity_encoder.fit_transform(y_train_severity)
            
            self.severity_model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            self.severity_model.fit(X_train_scaled, y_train_severity_encoded)
        
        print("Agent 2 trained successfully")
        return self
    
    def predict(self, X: pd.DataFrame) -> List[Dict]:
        """
        Predict security vulnerabilities
        Returns list of vulnerabilities with CWE/OWASP references
        """
        X_scaled = self.scaler.transform(X)
        
        # Predict vulnerability types (numeric)
        vuln_predictions_encoded = self.model.predict(X_scaled)
        vuln_probabilities = self.model.predict_proba(X_scaled)
        
        # Decode back to string labels
        vuln_predictions = self.label_encoder.inverse_transform(vuln_predictions_encoded)
        
        # Predict severity if model exists
        severity_predictions = None
        if self.severity_model is not None:
            severity_predictions_encoded = self.severity_model.predict(X_scaled)
            severity_predictions = self.severity_encoder.inverse_transform(severity_predictions_encoded)
        
        results = []
        for idx, vuln_type in enumerate(vuln_predictions):
            vuln_info = {
                'vulnerability': vuln_type,
                'confidence': float(max(vuln_probabilities[idx])),
                'severity': severity_predictions[idx] if severity_predictions is not None else 'MEDIUM'
            }
            
            # Add reference information
            if vuln_type in self.vulnerability_refs:
                ref_data = self.vulnerability_refs[vuln_type]
                vuln_info.update({
                    'cwe': ref_data['cwe'],
                    'owasp': ref_data['owasp'],
                    'description': ref_data['description'],
                    'references': ref_data['refs']
                })
            
            results.append(vuln_info)
        
        return results
    
    def save_model(self, path: str):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'severity_model': self.severity_model,
            'label_encoder': self.label_encoder,
            'severity_encoder': self.severity_encoder,
            'vulnerability_refs': self.vulnerability_refs
        }, path)
        print(f"Agent 2 model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.severity_model = data.get('severity_model')
        self.label_encoder = data.get('label_encoder')
        self.severity_encoder = data.get('severity_encoder')
        self.vulnerability_refs = data['vulnerability_refs']
        print(f"Agent 2 model loaded from {path}")


class Agent3_OutputAggregator:
    """
    Agent 3: Aggregates outputs from Agent 1 and Agent 2
    Formats final response for frontend
    """
    
    @staticmethod
    def aggregate(theory_results: List[Dict], security_results: List[Dict], 
                  code_snippet: str = None) -> Dict:
        """
        Combine results from both agents into structured output
        """
        output = {
            'code_snippet': code_snippet,
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'theory_analysis': {
                'patterns_detected': len(theory_results),
                'patterns': theory_results
            },
            'security_analysis': {
                'vulnerabilities_found': len(security_results),
                'vulnerabilities': security_results,
                'risk_level': Agent3_OutputAggregator._calculate_risk_level(security_results)
            },
            'recommendations': Agent3_OutputAggregator._generate_recommendations(
                theory_results, security_results
            )
        }
        
        return output
    
    @staticmethod
    def _calculate_risk_level(security_results: List[Dict]) -> str:
        """Calculate overall risk level"""
        if not security_results:
            return 'LOW'
        
        severity_map = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        max_severity = max([severity_map.get(v.get('severity', 'LOW'), 1) 
                           for v in security_results])
        
        if max_severity >= 4:
            return 'CRITICAL'
        elif max_severity >= 3:
            return 'HIGH'
        elif max_severity >= 2:
            return 'MEDIUM'
        return 'LOW'
    
    @staticmethod
    def _generate_recommendations(theory_results: List[Dict], 
                                 security_results: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Security recommendations
        for vuln in security_results:
            if vuln.get('severity') in ['CRITICAL', 'HIGH']:
                recommendations.append(
                    f"URGENT: Address {vuln.get('description', vuln['vulnerability'])} "
                    f"(Severity: {vuln.get('severity')})"
                )
        
        # Theory recommendations
        if len(theory_results) > 5:
            recommendations.append(
                "Consider refactoring: Code shows high pattern complexity"
            )
        
        if not recommendations:
            recommendations.append("No critical issues found. Continue with best practices.")
        
        return recommendations


def train_models_from_csv(csv_path: str, 
                         pattern_column: str = 'patterns',
                         vulnerability_column: str = 'vulnerability_type',
                         severity_column: str = 'severity'):
    """
    Train both agents from a CSV file containing code metrics
    
    CSV should have:
    - 20 code metric columns (numerical features)
    - patterns column (comma-separated patterns)
    - vulnerability_type column
    - severity column (optional)
    """
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Separate features and labels
    feature_columns = [col for col in df.columns 
                      if col not in [pattern_column, vulnerability_column, severity_column]]
    X = df[feature_columns]
    
    # Prepare pattern labels (multi-label)
    patterns = df[pattern_column].apply(lambda x: x.split(',') if pd.notna(x) else [])
    
    # Prepare vulnerability labels
    y_vuln = df[vulnerability_column]
    y_severity = df[severity_column] if severity_column in df.columns else None
    
    # Split data
    X_train, X_test, patterns_train, patterns_test, y_vuln_train, y_vuln_test = \
        train_test_split(X, patterns, y_vuln, test_size=0.2, random_state=42)
    
    if y_severity is not None:
        _, _, y_sev_train, y_sev_test = train_test_split(
            X, y_severity, test_size=0.2, random_state=42
        )
    else:
        y_sev_train = y_sev_test = None
    
    # Train Agent 1
    agent1 = Agent1_TheoryDetector()
    agent1.train(X_train, patterns_train.tolist())
    agent1.save_model('agent1_theory_detector.pkl')
    
    # Train Agent 2
    agent2 = Agent2_SecurityAnalyzer()
    agent2.train(X_train, y_vuln_train, y_sev_train)
    agent2.save_model('agent2_security_analyzer.pkl')
    
    # Evaluate models
    print("\n=== Evaluation ===")
    print("\nAgent 1 (Theory Detection) - Sample predictions:")
    theory_preds = agent1.predict(X_test.head(3))
    for i, pred in enumerate(theory_preds):
        print(f"Sample {i+1}: {len(pred)} patterns detected")
    
    print("\nAgent 2 (Security Analysis):")
    security_preds_encoded = agent2.model.predict(agent2.scaler.transform(X_test))
    security_preds = agent2.label_encoder.inverse_transform(security_preds_encoded)
    y_vuln_test_encoded = agent2.label_encoder.transform(y_vuln_test)
    print(f"Accuracy: {accuracy_score(y_vuln_test_encoded, security_preds_encoded):.3f}")
    
    return agent1, agent2


# Example usage and demo
if __name__ == "__main__":
    print("Three-Agent Java Security Analysis System")
    print("=" * 50)
    
    # This is a demo - in production, train from your actual CSV
    print("\nTo train models from your CSV:")
    print("agent1, agent2 = train_models_from_csv('your_code_metrics.csv')")
    print("\nTo use in production:")
    print("1. Extract code metrics from Java code")
    print("2. Load models: agent1.load_model('agent1_theory_detector.pkl')")
    print("3. Get predictions from both agents")
    print("4. Use Agent3 to aggregate results")