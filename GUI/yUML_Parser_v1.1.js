var FILENAME = "classes.json";

var json;
var classes = [];

upload(FILENAME);

function executeRestOfTheScript() {
    var classData = json;
    var newClass = createEmptyClass()
        .setName(classData.className)
        .setClassModifiers(classData.classModifiers)
        .setConstructors(classData.constructors)
        .addFields(classData.fields)
        .addInterfaces(classData.implementedInterfacesNames)
        .addMethods(classData.methods)
        .setParentClass(classData.extendedClassName);
    classes.push(newClass);
    // download( printDiagram() , 'output.txt' , 'txt');
    console.log(document.getElementById('yuml'));
    document.getElementById('yuml').src= "http://yuml.me/kompikosckrzy/diagram/scruffy/class/" + printDiagram();
}

function printDiagram() {
    var buffer = '';
    for (var i = 0 ; i < classes.length ; i++ ){
        if (classes[i].parentClass || classes[i].interfaces !== []) {
            if (classes[i].parentClass ){
                buffer += classes[i].printInheritance() + ',';
            }
            if ( classes[i].interfaces !== []) {
                buffer += classes[i].printInterfaces() ;
            }
        }
        else {
            buffer += classes[i].printClass();
            if (i != classes.length - 1){
                buffer += ',';
            }
        }
    }
    return buffer;
}

function upload(filename) {
    var client = new XMLHttpRequest();
    client.open('GET', './' + filename);
    client.onreadystatechange = function() {
        if (client.readyState == 4) {
            json = JSON.parse(client.responseText);
            executeRestOfTheScript();
        }
    };
    client.send();
}

function createEmptyClass() {
    return {
        printClass: function () {
            return "["
                + ((this.classModifiers === [] ) ? '' : this.printClassModifiers() )
                + this.name
                + ((this.constructors === [] ) ? '' : '|' + this.printConstructors() )
                + ((this.fields === [] ) ? '' : '|' + this.printFields() ) 
                + ((this.methods === [] ) ? '' : '|' + this.printMethods() )
                + "]"
        },
        setName: function (name) {
            this.name = name;
            return this;
        },
        setClassModifiers: function (modifiers) {
            var self = this;
            modifiers.forEach(function (T, number, array) {
               self.classModifiers.push(T);
            });
            return this
        },
        setConstructors: function (constructors) {
            var self = this;
            constructors.forEach(function (el, number, array) {
                self.constructors.push(el);
            });
            return this;
        },
        addFields: function (fields) {
            var self = this;
            fields.forEach(function (el) {
                self.fields.push(el)
            });
            return this;
        },
        addMethods: function (methods) {
            var self = this;
            methods.forEach(function (el) {
                self.methods.push(el)
            });
            return this;
        },
        setParentClass: function (parentClass) {
            this.parentClass = parentClass;
            return this;
        },
        addInterfaces: function (interfaces) {
            var self = this;
            interfaces.forEach(function (el) {
                self.interfaces.push(el)
            });
            return this;
        },
        printClassModifiers: function () {
            var buffer = '';
            this.classModifiers.forEach(function (modifier, index, array){
                switch (modifier){
                    case 'private':
                        buffer += '-';
                        break;
                    case 'package':
                        buffer += '~';
                        break;
                    case 'protected':
                        buffer += '＃';
                        break;
                    case 'public':
                        buffer += '+';
                        break;
                    case 'static':
                        buffer += 'static ';
                        break;
                    default :
                        console.log('Undefiend modifier attribute in class: ' + this.name);
                }
            });
            return buffer;
        },
        printConstructors: function () {
            var self = this;
            function methodToString(constructor) {

                var buffer = '';

                function printArguments() {
                    var buffer2 = '';

                    buffer2 += '(';
                    if (constructor.arguments){
                        for (var i = 0 ; i < constructor.arguments.length ; i++){
                            buffer2 += constructor.arguments[i][1] + ':' + constructor.arguments[i][0];
                            if (i != constructor.arguments.length-1){buffer2+=','}
                        }
                    }
                    buffer2 += ')';

                    return buffer2;
                }

                //add scope indicator

                constructor.modifiers.forEach(function( constructors, index, array ){
                    switch (constructors){
                        case 'private':
                            buffer += '-';
                            break;
                        case 'package':
                            buffer += '~';
                            break;
                        case 'protected':
                            buffer += '＃';
                            break;
                        case 'public':
                            buffer += '+';
                            break;
                        case 'static':
                            buffer += 'static ';
                            break;
                        default :
                            console.log('Undefiend modifier attribute in field: ' + self.name);
                    }
                });
                //end of scope indicator

                //add name
                buffer += self.name;

                // print () and arguments
                buffer += printArguments();

                //add type if provided

                return buffer;
            }
            var buffer = '';
            this.methods.forEach(function (el,index,array) {
                // console.log(el);
                buffer += methodToString(el) + ';';
            });
            // console.log(buffer);
            return buffer;
        },
        printFields: function () {
            function fieldToString(field) {
                var buffer2 = '';

                //add scope indicator
                field.modifiers.forEach(function( modifier, index, array){
                    switch (modifier){
                        case 'private':
                            buffer2 += '-';
                            break;
                        case 'package':
                            buffer2 += '~';
                            break;
                        case 'protected':
                            buffer2 += '＃';
                            break;
                        case 'public':
                            buffer2 += '+';
                            break;
                        case 'static':
                            buffer2 += 'static ';
                            break;
                        default :
                            console.log('Undefiend modifier attribute in field: ' + field.fieldName);
                    }
                });
                //end of scope indicator

                //add name
                buffer2 += field.fieldName + ' ';

                //add type if provided
                if (field.typeName !== '' ) {

                    //start with adding :
                    buffer2 += ':';
                    //if is list, add List tag
                    buffer2 += ((field.isCollection === true) ? 'List＜' : '');
                    //add type
                    buffer2 += field.typeName;
                    //if is list, close List tag
                    buffer2 += ((field.isCollection === true) ? '＞' : '');

                }

                return buffer2;
            }
            var buffer = '';
            this.fields.forEach(function (el,index,array) {
                buffer += fieldToString(el) + ';';
            });
            // console.log(buffer);
            return buffer;
        },
        printMethods: function () {
            function methodToString(method) {

                var buffer = '';

                function printArguments() {
                    var buffer2 = '';

                    buffer2 += '(';
                    if (method.arguments){
                        for (var i = 0 ; i < method.arguments.length ; i++){
                            buffer2 += method.arguments[i][1] + ':' + method.arguments[i][0];
                            if (i != method.arguments.length-1){buffer2+=','}
                        }
                    }
                    buffer2 += ')';

                    return buffer2;
                }

                //add scope indicator

                method.modifiers.forEach(function( modifier, index, array ){
                    switch (modifier){
                        case 'private':
                            buffer += '-';
                            break;
                        case 'package':
                            buffer += '~';
                            break;
                        case 'protected':
                            buffer += '＃';
                            break;
                        case 'public':
                            buffer += '+';
                            break;
                        case 'static':
                            buffer += 'static ';
                            break;
                        default :
                            console.log('Undefiend modifier attribute in field: ' + method.name);
                    }
                });
                //end of scope indicator

                //add name
                buffer += method.name;

                // print () and arguments
                buffer += printArguments();

                //add type if provided
                if (method.returnType !== '' ) {
                    // add type
                    buffer += ':' + method.returnType;
                }
                return buffer;
            }
            var buffer = '';
            this.methods.forEach(function (el,index,array) {
                // console.log(el);
                buffer += methodToString(el) + ';';
            });
            // console.log(buffer);
            return buffer;
        },
        printInheritance: function () {
            var buffer = '';

            buffer += '[' + this.parentClass + ']^-' + this.printClass();
            return buffer;
        },
        printInterfaces:  function () {
            var buffer = '';
            var self = this;

            this.interfaces.forEach(function (el, number, array) {
                buffer += '[﹤﹤interface﹥﹥' + el + ']^-.-' + self.printClass() + ',';
            });

            return buffer;
        },
        name: '',
        classModifiers: [],
        constructors: [],
        fields: [],
        methods: [],
        parentClass:'',
        interfaces: []
    }
}

function download(text, name, type) {
    var a = document.getElementById("downloadResults");
    var file = new Blob([text], {type: type});
    a.href = URL.createObjectURL(file);
    a.download = name;
}
