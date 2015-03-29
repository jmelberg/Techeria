$(function() {
                 var availableTags = [
                 "Adobe Test and Target",
                 "Google AdWords",
                 "MailChimp",
                 "Marketo",
                 "Microsoft Excel",
                 "SalesForce",
                 "SurveyMonkey",
                 ];
                 $( "#marketingtools" ).autocomplete({
                  source: availableTags
                });
               });