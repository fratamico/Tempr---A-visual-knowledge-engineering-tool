function toggle(source) {
        checkboxes = document.getElementsByName('aca');
        for(var i=0, n=checkboxes.length;i<n;i++) {
          if (source.checked === false) {
            checkboxes[i].checked = source.checked;
          }
          var parentID = checkboxes[i].parentElement.parentElement.parentElement.id;
          if (parentID === "raw_log_events") {
            if (checkboxes[i].offsetParent !== null) {
              checkboxes[i].checked = source.checked;
            }
          }
        }
      }  

function check_all(source) {
        checkboxes = document.getElementsByName('aca');
        for(var i=0, n=checkboxes.length;i<n;i++) {
          var parentID = checkboxes[i].parentElement.parentElement.parentElement.id;
          if (parentID === "raw_log_events") {
            if (checkboxes[i].offsetParent !== null) {
              checkboxes[i].checked = true;
            }
          }
        }
        source.checked = false;
      } 

$(function(){

        $('#merge_button').click(function(){


          var merged_name = document.getElementById('merge_name').value;
          document.getElementById('merge_name').value = "";

          var merged_items = $("input:checkbox[name=aca]:checked").map(function(){return $(this).val()}).get();

        //create new list item
        var merged_list = document.getElementById('merged_list');

        var entry = document.createElement('li');

        var input = document.createElement('input');
        input.setAttribute("type", "checkbox");
        input.setAttribute("value", merged_name);
        input.setAttribute("label", merged_name);
        input.setAttribute("name", "aca");
        entry.appendChild(input)
        entry.appendChild(document.createTextNode(" " + merged_name));

        var sublist = document.createElement('ul');
        entry.appendChild(sublist);

        for (var i=0; i < merged_items.length; i++){
          var subentry = document.createElement('li');
          subentry.appendChild(document.createTextNode(merged_items[i]));
          subentry.setAttribute("class", merged_name.replace(" ", "_") + "_mergedActionList");
          sublist.appendChild(subentry);
        }
        
        merged_list.appendChild(entry);

        //uncheck all boxes
        var cbarray = document.getElementsByName("aca");
        for(var i = 0; i < cbarray.length; i++){
          cbarray[i].checked = false;
        };

      });

        $('#popupclose').click(function(){


          $('#popup').hide("slow");

        });

      });

      //to filter the raw list of events
        $('#filter_raw_list').keyup(function(){
         var valThis = $(this).val().toLowerCase();
         if(valThis == ""){
          $('.filterable_list > li').show();           
        } else {
          $('.filterable_list > li').each(function(){
            var text = $(this).text().toLowerCase();
            (text.indexOf(valThis) >= 0) ? $(this).show() : $(this).hide();
          });
        };
      });