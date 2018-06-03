import ply.lex as lex
import ply.yacc as yacc
from Model import *
keywords = ('class', 'void', 'extends', 'implements', 'import', 'byte', 'short', 'int',
                'long', 'char', 'float', 'double', 'boolean', 'final',
                'public', 'protected', 'private', 'abstract', 'static', 'throws', 'package', 'String')

model = Model()
file = open("test.java", "r")
text = file.read()

class JavaBasicLexer:
    keywords = ('class', 'void', 'extends', 'implements', 'import', 'byte', 'short', 'int',
                'long', 'char', 'float', 'double', 'boolean', 'final',
                'public', 'protected', 'private', 'abstract', 'static', 'throws', 'package', 'String')

    tokens = [
                 'NAME',
                 'NUM',
                 'CHAR_LITERAL',
                 'STRING_LITERAL',
                 'LINE_COMMENT', 'BLOCK_COMMENT'
             ] + [k.upper() for k in keywords]

    literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

    t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

    t_ignore_LINE_COMMENT = '//.*'

    def t_BLOCK_COMMENT(t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    t_ignore = ' \t\f'

    def t_NAME(t):
        '[A-Za-z_$][A-Za-z0-9_$\.]*'
        if t.value in keywords:
            t.type = t.value.upper()
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def p_error(t):
        print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)

    def p_start(p):
        """start : package_declaration imports_declaration class_declaration"""
        print("package", p[1])
        print("imports", p[2])

    def p_package(p):
        """package_declaration : PACKAGE NAME ';'"""
        p[0] = p[2]

    def p_imports(p):
        """imports_declaration : imports_declaration import_declaration
                   | import_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_import(p):
        """import_declaration : IMPORT STATIC NAME ';'
                              | IMPORT STATIC NAME '*' ';'
                              | IMPORT NAME ';'
                              | IMPORT NAME '*' ';'"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[2] + p[3]

    def p_class_declaration(p):
        """class_declaration : modifiers CLASS NAME extends_declaration implement_declarations '{' class_body_elements '}'"""
        model.className = p[3]
        model.classModifiers = p[1]

    def p_extends_declaration(p):
        """extends_declaration : EXTENDS NAME
                               | """
        if len(p) > 1:
            model.extendedClassName = p[2]

    def p_implement_declarations(p):
        """implement_declarations : IMPLEMENTS interfaces
                                  | """
        if len(p) > 1:
            model.implementedInterfacesNames = p[2]
            print("class implements: ", p[2])

    def p_interfaces(p):
        """interfaces : NAME ',' interfaces
                      | NAME"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[3] + [p[1]]

    def p_class_body_elements(p):
        """class_body_elements : class_body_elements class_body_element
                                | class_body_element"""

    def p_class_body_element(p):
        """class_body_element : field_declaration
                              | method_declaration
                              | constructor_declaration
                              | BLOCK_COMMENT
                              | LINE_COMMENT"""

    def p_method_declaration(p):
        """method_declaration : modifiers VOID NAME '(' ')' throws_declaration '{' '}'
                              | modifiers VOID NAME '(' arguments_declaration ')' throws_declaration '{' '}'
                              | modifiers NAME NAME '(' ')' throws_declaration '{' '}'
                              | modifiers NAME NAME '(' arguments_declaration ')' throws_declaration '{' '}'
                              | modifiers primitive_type NAME '(' ')' throws_declaration '{' '}'
                              | modifiers primitive_type NAME '(' arguments_declaration ')' throws_declaration '{' '}'"""
        if p[5] == ')':
            print("Method declaration: ", p[3], "with return type", p[2])
            method = model.Method()
            method.modifiers = p[1]
            method.returnType = p[2]
            method.name = p[3]
            model.methods = model.methods + [method]
        else:
            print("Method declaration: ", p[3], "with return type", p[2], "and arguments:", p[5])
            method = model.Method()
            method.modifiers = p[1]
            method.returnType = p[2]
            method.name = p[3]
            method.arguments = p[5]
            model.methods = model.methods + [method]

    def p_throws_declaration(p):
        """throws_declaration : THROWS NAME
                              | """
        if len(p) > 1:
            p[0] = p[2]

    def p_constructor_declaration(p):
        """constructor_declaration : modifiers NAME '(' ')' '{' '}'
                                   | modifiers NAME '(' arguments_declaration ')' '{' '}'"""
        if len(p) == 7:
            print("Constructor", p[1], p[2])
            constructor = model.Constructor()
            constructor.modifiers = p[1]
            model.constructors = model.constructors + [constructor]
        else:
            print("Constructor", p[1], p[2], "with arguments", p[4])
            constructor = model.Constructor()
            constructor.modifiers = p[1]
            constructor.arguments = p[4]
            model.constructors = model.constructors + [constructor]

    def p_arguments_declaration(p):
        """arguments_declaration : argument ',' arguments_declaration
                      | argument"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[3] + [p[1]]

    def p_argument(p):
        """argument : primitive_type NAME
                    | NAME NAME"""
        p[0] = [p[1], p[2]]


    def p_field_declaration(p):
        """field_declaration : primitive_type_declaration
                             | list_type_declaration
                             | having_type_declaration
                             | array_type_declaration"""

    def p_primitive_type_declaration(p):
        """primitive_type_declaration : modifiers primitive_type NAME ';'"""
        print("field: ", p[1], p[2], p[3])
        field = model.Field()
        field.fieldName = p[3]
        field.isCollection = False
        field.isPrimitive = True
        field.typeName = p[2]
        field.modifiers = p[1]
        model.fields = model.fields + [field]


    def p_list_type_declaration(p):
        """list_type_declaration : modifiers NAME '<' NAME '>' NAME ';'"""
        print("Collection: ", p[2], "of", p[4], "named", p[6])
        field = model.Field()
        field.fieldName = p[6]
        field.isCollection = True
        field.isPrimitive = False
        field.typeName = p[4]
        field.modifiers = p[1]
        model.fields = model.fields + [field]

    def p_having_type_declaration(p):
        """having_type_declaration : modifiers NAME NAME ';'"""
        print("Class contains one to one relation with:", p[2])
        field = model.Field()
        field.fieldName = p[3]
        field.isCollection = False
        field.isPrimitive = False
        field.typeName = p[2]
        field.modifiers = p[1]
        model.fields = model.fields + [field]

    def p_array_type_declaration(p):
        """array_type_declaration : modifiers primitive_type '[' ']' NAME ';'
                                  | modifiers primitive_type NAME '[' ']' ';'
                                  | modifiers NAME '[' ']' NAME ';'
                                  | modifiers NAME NAME '[' ']' ';'"""

        if p[3] == '[':
            print ("Array of type:", p[2], "with name", p[5])
            field = model.Field()
            field.fieldName = p[5]
            field.isCollection = True
            if field.typeName in keywords:
                field.isPrimitive = True
            field.typeName = p[2]
            field.modifiers = p[1]
            model.fields = model.fields + [field]
        else:
            print ("Array of type:", p[2], "with name", p[3])
            field = model.Field()
            field.fieldName = p[3]
            field.isCollection = True
            if field.typeName in keywords:
                field.isPrimitive = True
            field.typeName = p[2]
            field.modifiers = p[1]
            model.fields = model.fields + [field]

    def p_primitive_type(p):
        """primitive_type : INT
                          | FLOAT
                          | SHORT
                          | CHAR
                          | STRING
                          | BYTE
                          | LONG
                          | DOUBLE
                          | BOOLEAN"""
        p[0] = p[1]

    def p_modifiers(p):
        """modifiers : modifier
                     | modifiers modifier"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_modifier(p):
        """modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | """
        if len(p) > 1:
            p[0] = p[1]



    lexer = lex.lex()
    parser = yacc.yacc()
    parser.parse(text, lexer=lexer)

    output_json = open("output.json", "w")
    output_json.write(model.to_json())
    output_json.close()


    print(model.to_json())