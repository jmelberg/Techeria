$(function() {
                 var availableTags = [
                 "Consumer Barometer",
                 "Feedly",
                 "GetResponse",
                 "Microsoft Excel",
                 "SalesForce",
                 "Vend",
                 ];
                 $( "#salestools" ).autocomplete({
                  source: availableTags
                });
               });