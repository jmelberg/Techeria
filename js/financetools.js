$(function() {
                 var availableTags = [
                 "Adaxa Suite",
                 "Adempiere",
                 "Apache OFBiz",
                 "Microsoft Excel",
                 "SalesForce",
                 ];
                 $( "#financetools" ).autocomplete({
                  source: availableTags
                });
               });