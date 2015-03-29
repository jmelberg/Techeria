$(function() {
                 var availableTags = [
                 "ActionScript",
                 "AppleScript",
                 "Asp",
                 "BASIC",
                 "C",
                 "C++",
                 "Clojure",
                 "COBOL",
                 "ColdFusion",
                 "Erlang",
                 "Fortran",
                 "Groovy",
                 "Go",
                 "Haskell",
                 "Java",
                 "JavaScript",
                 "Lisp",
                 "Objective C",
                 "Perl",
                 "PHP",
                 "Python",
                 "Ruby",
                 "Scala",
                 "Scheme",
                 "Swift",
                 ];
                 $( "#languages" ).autocomplete({
                  source: availableTags
                });
               });