import ast
from app.entities.api_list import APIList

class PythonAnalyzer(ast.NodeVisitor):
    def __init__(self, api_list: APIList):
        self.api_list = api_list    # Working APIList object
        self.variableNames = []      # List of variable names and their corresponding class names
        
        # From APIList get a list of just the class names
        # TODO: This is already done in the APIList class. Move this to APIList.
        self.classList = []
        for obj in self.api_list.getAPIObjectsList():
            if obj.getType() == 'class':
                className = obj.getName()
                self.classList.append(className)
        
        # From APIList get a list of just the method names
        self.methodNameList = []

    def analyze(self, rawCode: str):
        # Get the source code from the APIList object
        sourceCodeString = rawCode
        
        try:
            # Parse the source code into an AST
            tree = ast.parse(sourceCodeString)
        except SyntaxError as e:
            print(f"Skipping due to syntax error in source code: {e}")
            return self.api_list
        
        # Visit each node in the AST
        self.visit(tree)
        
        # Return the modified APIList object
        return self.api_list

    def visit_Assign(self, node):
        # Check for class instantiations within an Assign node
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute):
                className = func.attr # Class name
                if self.api_list.hasAPIObject(className) or self.api_list.hadAPIObectFullName(className):
                    self.api_list.incrementAPIObject(className) # Increment the appearances of the class
                    
                    # If there is a variable it is assigned to, keep track of the name
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variableName = target.id
                            self.variableNames.append((variableName, className))
        
        # Check for method calls within an Assign node
        self._extract_method_call(node.value)
        self.generic_visit(node)  # Continue traversing child nodes
    
    def visit_Expr(self, node):
        # Check for method calls within an Expr node
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute):
                # Check if the function is a method call on a tracked instance
                if isinstance(func.value, ast.Name):
                    variableName = func.value.id
                    for instance in self.variableNames:
                        if variableName == instance[0]:
                            # Get the instance name and method name
                            className = instance[1]
                            methodName = func.attr
                            fullName = className[1] + "." + methodName # method name matched with class name
                            if self.api_list.hasAPIObject(fullName):    # As it is stored in the APIList
                                self.api_list.incrementAPIObject(fullName)

    # Checks for class instantiations within a With statement
    def visit_With(self, node):
        if isinstance(node.items[0].context_expr, ast.Call):
            call = node.items[0].context_expr
            func = call.func
            if isinstance(func, ast.Attribute):
                className = func.attr
                if self.api_list.hasAPIObject(className) or self.api_list.hadAPIObectFullName(className):
                    self.api_list.incrementAPIObject(className)
                    if isinstance(node.items[0].optional_vars, ast.Name):
                        var_name = node.items[0].optional_vars.id
                        self.variableNames.append((var_name, className))

    # Check if the class is a subclass of another class
    def visit_ClassDef(self, node):
        for base in node.bases:
            class_name = self._extract_class_name_from_base(base)
            if class_name and (
                self.api_list.hasAPIObject(class_name) or 
                self.api_list.hadAPIObectFullName(class_name)
            ):
                self.api_list.incrementAPIObject(class_name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for direct instantiations like Connection()
        if isinstance(node.func, ast.Name):
            className = node.func.id
            if self.api_list.hasAPIObject(className) or self.api_list.hadAPIObectFullName(className):
                self.api_list.incrementAPIObject(className)
        self.generic_visit(node)  # Ensures method calls inside this call are still visited

    def visit_Try(self, node):
        # Check exception handlers (except blocks)
        for handler in node.handlers:
            if handler.type:
                # Case 1: Direct exception class (e.g., except TrackedException:)
                if isinstance(handler.type, ast.Name):
                    exc_name = handler.type.id
                    if self.api_list.hasAPIObject(exc_name) or self.api_list.hadAPIObectFullName(exc_name):
                        self.api_list.incrementAPIObject(exc_name)
                
                # Case 2: Exception class from module (e.g., except module.TrackedException:)
                elif isinstance(handler.type, ast.Attribute):
                    exc_name = self._get_attribute_name(handler.type)
                    if self.api_list.hasAPIObject(exc_name) or self.api_list.hadAPIObectFullName(exc_name):
                        self.api_list.incrementAPIObject(exc_name)
                
                # Case 3: Tuple of exceptions (e.g., except (TrackedException1, TrackedException2):)
                elif isinstance(handler.type, ast.Tuple):
                    for elt in handler.type.elts:
                        if isinstance(elt, ast.Name):
                            exc_name = elt.id
                            if self.api_list.hasAPIObject(exc_name) or self.api_list.hadAPIObectFullName(exc_name):
                                self.api_list.incrementAPIObject(exc_name)
                        elif isinstance(elt, ast.Attribute):
                            exc_name = self._get_attribute_name(elt)
                            if self.api_list.hasAPIObject(exc_name) or self.api_list.hadAPIObectFullName(exc_name):
                                self.api_list.incrementAPIObject(exc_name)
        
        # Continue visiting child nodes
        self.generic_visit(node)

    
    # Extract method calls from direct and chained calls. eg: methdod1().method2()
    def _extract_method_call(self, call_node):
        if not isinstance(call_node, ast.Call):
            return

        func = call_node.func
        if isinstance(func, ast.Attribute):
            # Case 1: Direct call like instance.method()
            if isinstance(func.value, ast.Name):
                variableName = func.value.id
                for var, cls in self.variableNames:
                    if variableName == var:
                        fullName = cls + "." + func.attr
                        if self.api_list.hasAPIObject(fullName):
                            self.api_list.incrementAPIObject(fullName)

            # Case 2: Chained call like instance.method1().method2()
            elif isinstance(func.value, ast.Call):
                inner_func = func.value.func
                if (
                    isinstance(inner_func, ast.Attribute) and
                    isinstance(inner_func.value, ast.Name)
                ):
                    inner_var = inner_func.value.id
                    for var, cls in self.variableNames:
                        if inner_var == var:
                            fullName = cls + "." + func.attr
                            if self.api_list.hasAPIObject(fullName):
                                self.api_list.incrementAPIObject(fullName)

    def _extract_class_name_from_base(self, base):
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return self._get_attribute_name(base)
        return None

    def _get_attribute_name(self, node):
        if isinstance(node, ast.Attribute):
            return self._get_attribute_name(node.value) + "." + node.attr
        elif isinstance(node, ast.Name):
            return node.id
        return ""


    def getAPIList(self):
        return self.api_list
    
    # For debugging purposes
    def printResults(self):
        print("\nParamiko Object Instantiations:")
        for i in self.instances:
            print(i)

        print("\nMethod Calls:")
        for i in self.method_calls:
            print(i)