"""
FIXED COMPREHENSIVE TEST SUITE
Matches the actual API response format from api_server.py
Run: python comprehensive_test_suite_fixed.py
"""

import requests
import json
from typing import Dict, List

class ComprehensiveTestSuite:
    """Test suite for all 48 theories and 7 security vulnerabilities"""
    
    def __init__(self, api_url: str = "http://localhost:5000/analyze"):
        self.api_url = api_url
        self.results = {
            'passed': [],
            'failed': [],
            'errors': []
        }
    
    def test_code(self, name: str, code: str, expected_patterns: List[str], 
                  expected_vulnerabilities: List[str] = None) -> bool:
        """Test a single code sample"""
        try:
            response = requests.post(
                self.api_url,
                json={'code': code},
                timeout=10
            )
            
            if response.status_code != 200:
                self.results['errors'].append({
                    'name': name,
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                })
                return False
            
            data = response.json()
            
            # ✅ FIXED: Extract detected patterns from correct location
            detected_patterns = []
            concept_analysis = data.get('conceptAnalysis', {})
            detected_concepts = concept_analysis.get('detectedConcepts', [])
            
            for concept in detected_concepts:
                # Get the pattern name
                name_field = concept.get('name', '')
                detected_patterns.append(name_field.lower())
            
            # ✅ FIXED: Extract detected vulnerabilities from correct location
            detected_vulns = []
            security = data.get('securityAnalysis', {})
            for vuln in security.get('vulnerabilities', []):
                vuln_type = vuln.get('type', '').lower().replace(' ', '_')
                detected_vulns.append(vuln_type)
            
            # If no vulnerabilities, it's considered 'none'
            if not detected_vulns:
                detected_vulns.append('none')
            
            # Check if expected patterns were found
            patterns_found = all(
                any(expected.lower() in detected for detected in detected_patterns)
                for expected in expected_patterns
            )
            
            # Check vulnerabilities if specified
            vulns_correct = True
            if expected_vulnerabilities is not None:
                if 'none' in expected_vulnerabilities:
                    # Expecting no vulnerabilities
                    vulns_correct = len(security.get('vulnerabilities', [])) == 0 or \
                                   detected_vulns == ['none']
                else:
                    # Expecting specific vulnerabilities
                    vulns_correct = any(
                        any(expected.lower() in detected.lower() for detected in detected_vulns)
                        for expected in expected_vulnerabilities
                    )
            
            success = patterns_found and vulns_correct
            
            result = {
                'name': name,
                'expected_patterns': expected_patterns,
                'detected_patterns': detected_patterns,
                'expected_vulnerabilities': expected_vulnerabilities or [],
                'detected_vulnerabilities': detected_vulns,
                'success': success
            }
            
            if success:
                self.results['passed'].append(result)
            else:
                self.results['failed'].append(result)
            
            return success
            
        except Exception as e:
            self.results['errors'].append({
                'name': name,
                'error': str(e)
            })
            return False
    
    def print_result(self, name: str, success: bool, detected: List[str]):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:12s} {name:50s}", end='')
        if detected:
            print(f" → {', '.join(detected[:2])}")
        else:
            print(" → No patterns detected")
    
    def run_all_tests(self):
        """Run all tests"""
        
        print("\n" + "="*100)
        print("COMPREHENSIVE TEST SUITE - ALL 48 THEORIES + 7 SECURITY VULNERABILITIES")
        print("="*100)
        
        # ========== CREATIONAL PATTERNS (5) ==========
        print("\n🎨 CREATIONAL DESIGN PATTERNS (5)")
        print("-"*100)
        
        # 1. Singleton
        singleton_code = """public class Database {
    private static Database instance;
    private Database() {}
    
    public static Database getInstance() {
        if (instance == null) {
            instance = new Database();
        }
        return instance;
    }
}"""
        success = self.test_code("Singleton Design Pattern", singleton_code, ['singleton'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Singleton Design Pattern"]
        self.print_result("Singleton Design Pattern", success, detected[0] if detected else [])
        
        # 2. Factory
        factory_code = """public class CarFactory {
    public static Car getCar(String type) {
        switch (type.toLowerCase()) {
            case "sedan": return new Sedan();
            case "suv": return new SUV();
            default: return null;
        }
    }
}"""
        success = self.test_code("Factory Design Pattern", factory_code, ['factory'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Factory Design Pattern"]
        self.print_result("Factory Design Pattern", success, detected[0] if detected else [])
        
        # 3. Builder
        builder_code = """public class User {
    private String name, email;
    
    public static class Builder {
        private String name, email;
        public Builder name(String n) { name = n; return this; }
        public Builder email(String e) { email = e; return this; }
        public User build() { return new User(this); }
    }
}"""
        success = self.test_code("Builder Design Pattern", builder_code, ['builder'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Builder Design Pattern"]
        self.print_result("Builder Design Pattern", success, detected[0] if detected else [])
        
        # 4. Prototype
        prototype_code = """public class Shape implements Cloneable {
    private String type;
    
    @Override
    public Shape clone() {
        try {
            return (Shape) super.clone();
        } catch (CloneNotSupportedException e) {
            return new Shape(this);
        }
    }
}"""
        success = self.test_code("Prototype Design Pattern", prototype_code, ['prototype'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Prototype Design Pattern"]
        self.print_result("Prototype Design Pattern", success, detected[0] if detected else [])
        
        # 5. Abstract Factory
        abstract_factory_code = """public interface GUIFactory {
    Button createButton();
    TextBox createTextBox();
}

public class WindowsFactory implements GUIFactory {
    public Button createButton() { return new WindowsButton(); }
    public TextBox createTextBox() { return new WindowsTextBox(); }
}"""
        success = self.test_code("Abstract Factory Design Pattern", abstract_factory_code, ['abstract_factory'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Abstract Factory Design Pattern"]
        self.print_result("Abstract Factory Design Pattern", success, detected[0] if detected else [])
        
        # ========== STRUCTURAL PATTERNS (7) ==========
        print("\n🏗️ STRUCTURAL DESIGN PATTERNS (7)")
        print("-"*100)
        
        # 6. Adapter
        adapter_code = """public class AudioAdapter implements MediaPlayer {
    private AdvancedMediaPlayer adaptee;
    
    public AudioAdapter(String type) {
        adaptee = new VLCPlayer();
    }
    
    public void play(String file) {
        adaptee.playVlc(file);
    }
}"""
        success = self.test_code("Adapter Design Pattern", adapter_code, ['adapter'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Adapter Design Pattern"]
        self.print_result("Adapter Design Pattern", success, detected[0] if detected else [])
        
        # 7. Decorator
        decorator_code = """public class BorderDecorator implements Component {
    private Component component;
    
    public BorderDecorator(Component c) {
        this.component = c;
    }
    
    public void draw() {
        component.draw();
        drawBorder();
    }
}"""
        success = self.test_code("Decorator Design Pattern", decorator_code, ['decorator'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Decorator Design Pattern"]
        self.print_result("Decorator Design Pattern", success, detected[0] if detected else [])
        
        # 8. Proxy
        proxy_code = """public class ProxyImage implements Image {
    private RealImage realImage;
    
    public void display() {
        if (checkAccess()) {
            realImage.display();
        }
    }
    
    private boolean checkAccess() { return true; }
}"""
        success = self.test_code("Proxy Design Pattern", proxy_code, ['proxy'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Proxy Design Pattern"]
        self.print_result("Proxy Design Pattern", success, detected[0] if detected else [])
        
        # 9. Composite
        composite_code = """public class Composite implements Component {
    private List<Component> children = new ArrayList<>();
    
    public void add(Component c) { children.add(c); }
    
    public void operation() {
        for (Component child : children) {
            child.operation();
        }
    }
}"""
        success = self.test_code("Composite Design Pattern", composite_code, ['composite'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Composite Design Pattern"]
        self.print_result("Composite Design Pattern", success, detected[0] if detected else [])
        
        # 10. Facade
        facade_code = """public class HomeFacade {
    private LightSystem lights;
    private SecuritySystem security;
    
    public void leaveHome() {
        lights.turnOff();
        security.arm();
    }
    
    public void arriveHome() {
        security.disarm();
        lights.turnOn();
    }
}"""
        success = self.test_code("Facade Design Pattern", facade_code, ['facade'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Facade Design Pattern"]
        self.print_result("Facade Design Pattern", success, detected[0] if detected else [])
        
        # 11. Bridge
        bridge_code = """public abstract class Shape {
    protected DrawingAPI implementation;
    
    protected Shape(DrawingAPI impl) {
        this.implementation = impl;
    }
    
    public abstract void draw();
}

public class Circle extends Shape {
    public void draw() { implementation.drawCircle(); }
}"""
        success = self.test_code("Bridge Design Pattern", bridge_code, ['bridge'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Bridge Design Pattern"]
        self.print_result("Bridge Design Pattern", success, detected[0] if detected else [])
        
        # 12. Flyweight
        flyweight_code = """public class CharacterFactory {
    private Map<Character, CharacterStyle> cache = new HashMap<>();
    
    public CharacterStyle getStyle(char c) {
        if (!cache.containsKey(c)) {
            cache.put(c, new CharacterStyle(c));
        }
        return cache.get(c);
    }
}"""
        success = self.test_code("Flyweight Design Pattern", flyweight_code, ['flyweight'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Flyweight Design Pattern"]
        self.print_result("Flyweight Design Pattern", success, detected[0] if detected else [])
        
        # ========== BEHAVIORAL PATTERNS (11) ==========
        print("\n🔄 BEHAVIORAL DESIGN PATTERNS (11)")
        print("-"*100)
        
        # 13. Strategy
        strategy_code = """public class PaymentContext {
    private PaymentStrategy strategy;
    
    public void setStrategy(PaymentStrategy s) {
        this.strategy = s;
    }
    
    public void pay(int amount) {
        strategy.processPayment(amount);
    }
}"""
        success = self.test_code("Strategy Design Pattern", strategy_code, ['strategy'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Strategy Design Pattern"]
        self.print_result("Strategy Design Pattern", success, detected[0] if detected else [])
        
        # 14. Observer
        observer_code = """public class NewsAgency {
    private List<Observer> observers = new ArrayList<>();
    
    public void attach(Observer o) { observers.add(o); }
    
    public void notifyObservers(String news) {
        for (Observer o : observers) {
            o.update(news);
        }
    }
}"""
        success = self.test_code("Observer Design Pattern", observer_code, ['observer'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Observer Design Pattern"]
        self.print_result("Observer Design Pattern", success, detected[0] if detected else [])
        
        # 15. Command
        command_code = """public class LightCommand implements Command {
    private Light receiver;
    
    public LightCommand(Light light) {
        this.receiver = light;
    }
    
    public void execute() {
        receiver.turnOn();
    }
}"""
        success = self.test_code("Command Design Pattern", command_code, ['command'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Command Design Pattern"]
        self.print_result("Command Design Pattern", success, detected[0] if detected else [])
        
        # 16. Template Method
        template_code = """public abstract class DataProcessor {
    public final void process() {
        loadData();
        processData();
        saveData();
    }
    
    protected abstract void processData();
    protected void loadData() { }
    protected void saveData() { }
}"""
        success = self.test_code("Template Method Design Pattern", template_code, ['template'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Template Method Design Pattern"]
        self.print_result("Template Method Design Pattern", success, detected[0] if detected else [])
        
        # 17. Iterator
        iterator_code = """public class BookIterator implements Iterator<Book> {
    private List<Book> books;
    private int position = 0;
    
    public boolean hasNext() {
        return position < books.size();
    }
    
    public Book next() {
        return books.get(position++);
    }
}"""
        success = self.test_code("Iterator Design Pattern", iterator_code, ['iterator'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Iterator Design Pattern"]
        self.print_result("Iterator Design Pattern", success, detected[0] if detected else [])
        
        # 18. State
        state_code = """public class Document {
    private State state;
    
    public void setState(State newState) {
        this.state = newState;
    }
    
    public void publish() {
        state.publish(this);
    }
}

interface State {
    void publish(Document doc);
}"""
        success = self.test_code("State Design Pattern", state_code, ['state'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "State Design Pattern"]
        self.print_result("State Design Pattern", success, detected[0] if detected else [])
        
        # 19. Chain of Responsibility
        chain_code = """public abstract class Handler {
    protected Handler nextHandler;
    
    public void setNext(Handler next) {
        this.nextHandler = next;
    }
    
    public void handleRequest(Request req) {
        if (nextHandler != null) {
            nextHandler.handleRequest(req);
        }
    }
}"""
        success = self.test_code("Chain of Responsibility Pattern", chain_code, ['chain'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Chain of Responsibility Pattern"]
        self.print_result("Chain of Responsibility Pattern", success, detected[0] if detected else [])
        
        # 20. Mediator
        mediator_code = """public class ChatMediator {
    private List<User> users = new ArrayList<>();
    
    public void sendMessage(String msg, User sender) {
        for (User user : users) {
            if (user != sender) {
                user.receive(msg);
            }
        }
    }
}"""
        success = self.test_code("Mediator Design Pattern", mediator_code, ['mediator'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Mediator Design Pattern"]
        self.print_result("Mediator Design Pattern", success, detected[0] if detected else [])
        
        # 21. Memento
        memento_code = """public class Originator {
    private String state;
    
    public Memento saveState() {
        return new Memento(state);
    }
    
    public void restoreState(Memento m) {
        this.state = m.getState();
    }
}

public class Caretaker {
    private Memento memento;
}"""
        success = self.test_code("Memento Design Pattern", memento_code, ['memento'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Memento Design Pattern"]
        self.print_result("Memento Design Pattern", success, detected[0] if detected else [])
        
        # 22. Visitor
        visitor_code = """public interface Visitor {
    void visit(Book book);
    void visit(Magazine magazine);
}

public class Book {
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}"""
        success = self.test_code("Visitor Design Pattern", visitor_code, ['visitor'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Visitor Design Pattern"]
        self.print_result("Visitor Design Pattern", success, detected[0] if detected else [])
        
        # 23. Interpreter
        interpreter_code = """public interface Expression {
    int interpret();
}

public class NumberExpression implements Expression {
    private int number;
    public int interpret() { return number; }
}

public class AddExpression implements Expression {
    public int interpret() { return left.interpret() + right.interpret(); }
}"""
        success = self.test_code("Interpreter Design Pattern", interpreter_code, ['interpreter'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Interpreter Design Pattern"]
        self.print_result("Interpreter Design Pattern", success, detected[0] if detected else [])
        
        # ========== SPRING FRAMEWORK PATTERNS (7) ==========
        print("\n🍃 SPRING FRAMEWORK PATTERNS (7)")
        print("-"*100)
        
        # 24. Dependency Injection
        di_code = """@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}"""
        success = self.test_code("Dependency Injection", di_code, ['dependency', 'injection'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Dependency Injection"]
        self.print_result("Dependency Injection", success, detected[0] if detected else [])
        
        # 25. Spring MVC
        mvc_code = """@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
    
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
}"""
        success = self.test_code("Spring MVC Pattern", mvc_code, ['spring', 'mvc'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Spring MVC Pattern"]
        self.print_result("Spring MVC Pattern", success, detected[0] if detected else [])
        
        # 26. RESTful API
        rest_code = """@RestController
@RequestMapping("/api/products")
public class ProductAPI {
    @GetMapping
    public List<Product> getAll() { return productService.findAll(); }
    
    @PostMapping
    public Product create(@RequestBody Product p) { return productService.save(p); }
    
    @PutMapping("/{id}")
    public Product update(@PathVariable Long id, @RequestBody Product p) {
        return productService.update(id, p);
    }
}"""
        success = self.test_code("RESTful API Pattern", rest_code, ['restful', 'api'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "RESTful API Pattern"]
        self.print_result("RESTful API Pattern", success, detected[0] if detected else [])
        
        # 27. Repository
        repo_code = """@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
    List<User> findByAgeGreaterThan(int age);
    
    @Query("SELECT u FROM User u WHERE u.status = :status")
    List<User> findByStatus(@Param("status") String status);
}"""
        success = self.test_code("Repository Pattern", repo_code, ['repository'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Repository Pattern"]
        self.print_result("Repository Pattern", success, detected[0] if detected else [])
        
        # 28. Service Layer
        service_code = """@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    
    @Transactional
    public Order createOrder(OrderDTO dto) {
        Order order = new Order();
        order.setItems(dto.getItems());
        return orderRepository.save(order);
    }
}"""
        success = self.test_code("Service Layer Pattern", service_code, ['service'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Service Layer Pattern"]
        self.print_result("Service Layer Pattern", success, detected[0] if detected else [])
        
        # 29. DTO
        dto_code = """public class UserDTO {
    private String username;
    private String email;
    
    public String getUsername() { return username; }
    public void setUsername(String u) { this.username = u; }
    public String getEmail() { return email; }
    public void setEmail(String e) { this.email = e; }
}"""
        success = self.test_code("DTO Pattern", dto_code, ['dto'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "DTO Pattern"]
        self.print_result("DTO Pattern", success, detected[0] if detected else [])
        
        # 30. AOP
        aop_code = """@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Before: " + joinPoint.getSignature());
    }
    
    @After("execution(* com.example.service.*.*(..))")
    public void logAfter() {
        System.out.println("Method executed");
    }
}"""
        success = self.test_code("AOP Pattern", aop_code, ['aop'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "AOP Pattern"]
        self.print_result("AOP Pattern", success, detected[0] if detected else [])
        
        # ========== CORE JAVA CONCEPTS (6) ==========
        print("\n☕ CORE JAVA CONCEPTS (6)")
        print("-"*100)
        
        # 31. OOP Fundamentals
        oop_code = """public class Animal {
    protected String name;
    public void makeSound() { }
}

public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}"""
        success = self.test_code("OOP Fundamentals", oop_code, ['oop'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "OOP Fundamentals"]
        self.print_result("OOP Fundamentals", success, detected[0] if detected else [])
        
        # 32. Collections Framework
        collections_code = """public class CollectionsExample {
    public void demonstrateCollections() {
        List<String> list = new ArrayList<>();
        list.add("Java");
        
        Set<Integer> set = new HashSet<>();
        set.add(1);
        
        Map<String, Integer> map = new HashMap<>();
        map.put("age", 25);
    }
}"""
        success = self.test_code("Collections Framework", collections_code, ['collections'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Collections Framework"]
        self.print_result("Collections Framework", success, detected[0] if detected else [])
        
        # 33. Exception Handling
        exception_code = """@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(ex.getMessage());
        return ResponseEntity.status(404).body(error);
    }
}"""
        success = self.test_code("Exception Handling", exception_code, ['exception'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Exception Handling"]
        self.print_result("Exception Handling", success, detected[0] if detected else [])
        
        # 34. Conditional Control Flow
        conditional_code = """public class DiscountCalculator {
    public double calculateDiscount(String customerType, double amount) {
        if (amount > 1000) {
            switch (customerType) {
                case "PREMIUM": return amount * 0.15;
                case "GOLD": return amount * 0.10;
                default: return amount * 0.05;
            }
        } else if (amount > 500) {
            return amount * 0.03;
        }
        return 0;
    }
}"""
        success = self.test_code("Conditional Control Flow", conditional_code, ['conditional'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Conditional Control Flow"]
        self.print_result("Conditional Control Flow", success, detected[0] if detected else [])
        
        # 35. Loops and Iteration
        loops_code = """public class LoopExamples {
    public void demonstrateLoops() {
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }
        
        List<String> items = Arrays.asList("A", "B", "C");
        for (String item : items) {
            System.out.println(item);
        }
        
        items.forEach(item -> System.out.println(item));
    }
}"""
        success = self.test_code("Loops and Iteration", loops_code, ['loops', 'iteration'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Loops and Iteration"]
        self.print_result("Loops and Iteration", success, detected[0] if detected else [])
        
        # 36. Basic Programming Constructs
        basic_code = """public class Calculator {
    private int value;
    
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
}"""
        success = self.test_code("Basic Programming Constructs", basic_code, ['basic'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Basic Programming Constructs"]
        self.print_result("Basic Programming Constructs", success, detected[0] if detected else [])
        
        # ========== MODERN JAVA FEATURES (2) ==========
        print("\n🔮 MODERN JAVA FEATURES (2)")
        print("-"*100)
        
        # 37. Optional & Null Safety
        optional_code = """public class UserService {
    public Optional<User> findUser(Long id) {
        return userRepository.findById(id);
    }
    
    public String getUserName(Long id) {
        return findUser(id)
            .map(User::getName)
            .orElse("Unknown");
    }
}"""
        success = self.test_code("Optional & Null Safety", optional_code, ['optional'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Optional & Null Safety"]
        self.print_result("Optional & Null Safety", success, detected[0] if detected else [])
        
        # 38. Functional Programming
        functional_code = """public class StreamExample {
    public List<String> processNames(List<String> names) {
        return names.stream()
            .filter(name -> name.length() > 3)
            .map(String::toUpperCase)
            .collect(Collectors.toList());
    }
    
    Function<Integer, Integer> square = x -> x * x;
}"""
        success = self.test_code("Functional Programming", functional_code, ['functional'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Functional Programming"]
        self.print_result("Functional Programming", success, detected[0] if detected else [])
        
        # ========== SPRING BOOT ECOSYSTEM (4) ==========
        print("\n🚀 SPRING BOOT ECOSYSTEM (4)")
        print("-"*100)
        
        # 39. Spring Boot Error Handling
        error_code = """@ControllerAdvice
public class GlobalErrorHandler {
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ValidationException ex) {
        return ResponseEntity.badRequest().body(new ErrorResponse(ex.getMessage()));
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        return ResponseEntity.status(500).body(new ErrorResponse("Internal error"));
    }
}"""
        success = self.test_code("Spring Boot Error Handling", error_code, ['error', 'handling'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Spring Boot Error Handling"]
        self.print_result("Spring Boot Error Handling", success, detected[0] if detected else [])
        
        # 40. Reactive Programming
        reactive_code = """@Service
public class UserService {
    @Autowired
    private WebClient webClient;
    
    public Mono<User> fetchUserAsync(Long userId) {
        return webClient.get()
            .uri("/users/{id}", userId)
            .retrieve()
            .bodyToMono(User.class);
    }
}"""
        success = self.test_code("Reactive Programming", reactive_code, ['reactive'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Reactive Programming"]
        self.print_result("Reactive Programming", success, detected[0] if detected else [])
        
        # 41. Utility Libraries
        util_code = """public class StringUtils {
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }
    
    public static String capitalize(String str) {
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }
}"""
        success = self.test_code("Utility Libraries", util_code, ['util'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Utility Libraries"]
        self.print_result("Utility Libraries", success, detected[0] if detected else [])
        
        # 42. Lombok & JPA
        lombok_code = """@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String username;
}"""
        success = self.test_code("Lombok & JPA Annotations", lombok_code, ['lombok', 'jpa'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Lombok & JPA Annotations"]
        self.print_result("Lombok & JPA Annotations", success, detected[0] if detected else [])
        
        # ========== WEB DEVELOPMENT (3) ==========
        print("\n🌐 WEB DEVELOPMENT (3)")
        print("-"*100)
        
        # 43. Core Annotations & DI
        core_anno_code = """@Component
public class EmailService {
    @Autowired
    private MailSender mailSender;
    
    @Value("${mail.from}")
    private String fromAddress;
    
    public void sendEmail(String to, String subject) {
        mailSender.send(to, subject);
    }
}"""
        success = self.test_code("Core Annotations & DI", core_anno_code, ['core', 'annotations'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Core Annotations & DI"]
        self.print_result("Core Annotations & DI", success, detected[0] if detected else [])
        
        # 44. Web MVC Annotations
        web_mvc_code = """@Controller
public class HomeController {
    @RequestMapping("/home")
    public String home(@RequestParam String name, Model model) {
        model.addAttribute("greeting", "Hello " + name);
        return "home";
    }
    
    @GetMapping("/user/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}"""
        success = self.test_code("Web MVC Annotations", web_mvc_code, ['web', 'mvc'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Web MVC Annotations"]
        self.print_result("Web MVC Annotations", success, detected[0] if detected else [])
        
        # 45. HTTP Request Processing
        http_code = """@RestController
public class ApiController {
    @PostMapping("/process")
    public ResponseEntity<Result> process(@RequestBody Request req) {
        Result result = processRequest(req);
        return ResponseEntity.ok(result);
    }
    
    @GetMapping("/data")
    public @ResponseBody Data getData(HttpServletRequest request) {
        return new Data(request.getParameter("id"));
    }
}"""
        success = self.test_code("HTTP Request Processing", http_code, ['http', 'request'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "HTTP Request Processing"]
        self.print_result("HTTP Request Processing", success, detected[0] if detected else [])
        
        # ========== API DOCUMENTATION (1) ==========
        print("\n📚 API DOCUMENTATION (1)")
        print("-"*100)
        
        # 46. OpenAPI
        openapi_code = """@RestController
@Api(tags = "User Management")
@RequestMapping("/api/users")
public class UserController {
    @ApiOperation(value = "Get user by ID")
    @ApiResponse(code = 200, message = "Success")
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}"""
        success = self.test_code("OpenAPI Documentation", openapi_code, ['openapi', 'api'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "OpenAPI Documentation"]
        self.print_result("OpenAPI Documentation", success, detected[0] if detected else [])
        
        # ========== DATABASE INTEGRATION (2) ==========
        print("\n🗃️ DATABASE INTEGRATION (2)")
        print("-"*100)
        
        # 47. Spring Data JPA
        jpa_code = """@Entity
public class Product {
    @Id
    @GeneratedValue
    private Long id;
    private String name;
}

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    @Query("SELECT p FROM Product p WHERE p.price > :price")
    List<Product> findExpensiveProducts(@Param("price") Double price);
}"""
        success = self.test_code("Spring Data JPA", jpa_code, ['spring', 'data', 'jpa'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Spring Data JPA"]
        self.print_result("Spring Data JPA", success, detected[0] if detected else [])
        
        # 48. Batch Processing
        batch_code = """@Configuration
@EnableBatchProcessing
public class BatchConfig {
    @Bean
    public Job importJob(JobBuilderFactory jobs, Step step) {
        return jobs.get("importJob").start(step).build();
    }
    
    @Bean
    public Step step(StepBuilderFactory steps, ItemReader<Data> reader) {
        return steps.get("step")
            .<Data, Data>chunk(100)
            .reader(reader)
            .processor(processor())
            .writer(writer())
            .build();
    }
}"""
        success = self.test_code("Batch Processing & ETL", batch_code, ['batch'])
        detected = [r['detected_patterns'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Batch Processing & ETL"]
        self.print_result("Batch Processing & ETL", success, detected[0] if detected else [])
        
        # ========== SECURITY VULNERABILITIES (7) ==========
        print("\n🛡️ SECURITY VULNERABILITIES (7)")
        print("-"*100)
        
        # 1. SQL Injection
        sql_injection_code = """public class UserDAO {
    public User findUser(String username) {
        String query = "SELECT * FROM users WHERE username = '" + username + "'";
        return jdbcTemplate.queryForObject(query, User.class);
    }
}"""
        success = self.test_code("SQL Injection Vulnerability", sql_injection_code, [], ['sql_injection'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "SQL Injection Vulnerability"]
        self.print_result("SQL Injection Vulnerability", success, detected[0] if detected else [])
        
        # 2. XSS
        xss_code = """@GetMapping("/comment")
public String showComment(@RequestParam String text) {
    return "<div>" + text + "</div>";
}"""
        success = self.test_code("XSS Vulnerability", xss_code, [], ['xss'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "XSS Vulnerability"]
        self.print_result("XSS Vulnerability", success, detected[0] if detected else [])
        
        # 3. Path Traversal
        path_code = """public File getFile(String filename) {
    return new File("/uploads/" + filename);
}"""
        success = self.test_code("Path Traversal Vulnerability", path_code, [], ['path_traversal'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Path Traversal Vulnerability"]
        self.print_result("Path Traversal Vulnerability", success, detected[0] if detected else [])
        
        # 4. XXE
        xxe_code = """public Document parseXML(String xml) {
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    return builder.parse(new InputSource(new StringReader(xml)));
}"""
        success = self.test_code("XXE Vulnerability", xxe_code, [], ['xxe'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "XXE Vulnerability"]
        self.print_result("XXE Vulnerability", success, detected[0] if detected else [])
        
        # 5. Authentication Bypass
        auth_code = """@PostMapping("/login")
public String login(@RequestParam String user, @RequestParam String pass) {
    if (user.equals("admin") && pass.length() > 5) {
        return "success";
    }
    return "failed";
}"""
        success = self.test_code("Authentication Bypass", auth_code, [], ['authentication_bypass'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Authentication Bypass"]
        self.print_result("Authentication Bypass", success, detected[0] if detected else [])
        
        # 6. Insecure Deserialization
        deser_code = """public Object deserialize(byte[] data) {
    ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
    return ois.readObject();
}"""
        success = self.test_code("Insecure Deserialization", deser_code, [], ['insecure_deserialization'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Insecure Deserialization"]
        self.print_result("Insecure Deserialization", success, detected[0] if detected else [])
        
        # 7. Secure State (No Vulnerabilities)
        secure_code = """@RestController
public class SecureController {
    @Autowired
    private BCryptPasswordEncoder encoder;
    
    @PostMapping("/register")
    public User register(@Valid @RequestBody UserDTO dto) {
        User user = new User();
        user.setPassword(encoder.encode(dto.getPassword()));
        return userRepository.save(user);
    }
}"""
        success = self.test_code("Secure State (No Vulnerabilities)", secure_code, [], ['none'])
        detected = [r['detected_vulnerabilities'] for r in self.results['passed'] + self.results['failed'] if r['name'] == "Secure State (No Vulnerabilities)"]
        self.print_result("Secure State (No Vulnerabilities)", success, detected[0] if detected else [])
        
        # ========== SUMMARY ==========
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.results['passed']) + len(self.results['failed']) + len(self.results['errors'])
        passed = len(self.results['passed'])
        failed = len(self.results['failed'])
        errors = len(self.results['errors'])
        
        print("\n" + "="*100)
        print("TEST SUMMARY")
        print("="*100)
        print(f"Total Tests:  {total}")
        print(f"✅ Passed:    {passed} ({passed*100//total if total > 0 else 0}%)")
        print(f"❌ Failed:    {failed} ({failed*100//total if total > 0 else 0}%)")
        print(f"⚠️  Errors:    {errors} ({errors*100//total if total > 0 else 0}%)")
        
        if failed > 0:
            print("\n" + "-"*100)
            print("FAILED TESTS:")
            print("-"*100)
            for result in self.results['failed'][:10]:  # Show first 10
                print(f"\n❌ {result['name']}")
                print(f"   Expected: {result['expected_patterns']}")
                print(f"   Detected: {result['detected_patterns'][:3]}")
        
        if errors > 0:
            print("\n" + "-"*100)
            print("ERROR TESTS:")
            print("-"*100)
            for error in self.results['errors'][:5]:  # Show first 5
                print(f"\n⚠️  {error['name']}")
                print(f"   Error: {error.get('error', 'Unknown')}")
        
        print("\n" + "="*100)
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your system is working perfectly!")
        elif passed > total * 0.8:
            print("👍 Most tests passed! Minor issues to fix.")
        elif passed > total * 0.5:
            print("⚠️  Some tests failed. Review detection logic.")
        else:
            print("❌ Many tests failed. Check model training and detection logic.")
        print("="*100)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                        FIXED COMPREHENSIVE TEST SUITE                                          ║
║                      Now matches actual API response format                                    ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    suite = ComprehensiveTestSuite()
    
    # Run a quick connection test first
    print("Testing API connection...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running\n")
        else:
            print(f"⚠️  API returned status {response.status_code}\n")
    except:
        print("❌ Cannot connect to API server!")
        print("   Make sure to run: python api_server.py\n")
        exit(1)
    
    suite.run_all_tests()