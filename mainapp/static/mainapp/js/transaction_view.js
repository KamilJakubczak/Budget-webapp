
var all_types = document.querySelectorAll(".type")
console.log(all_types.length)

for(i=1;i<=all_types.length;i++){
	let type_id = "#id_types_"+i 
	let category_id = "#id_category_"+i
	let payment_id = "#id_payment_"+i
	debugger
	$(type_id).change(function () {

      var url = $("#myTable").attr("data-types-url");  // get the url of the `load_cities` view
      var typeId = $(this).val();  // get the selected country ID from the HTML input
      //console.log(typeId)
     
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'type': typeId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $(category_id).html(data); 
          //console.log('data',data) // replace the contents of the city input with the data that came from the server
        }
      });

      var url2 = $("#myTable").attr("data-payments-url");  // get the url of the `load_cities` view
    
      $.ajax({                       // initialize an AJAX request
        url: url2,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'payment': typeId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $(payment_id).html(data); 
          //console.log('data',data) // replace the contents of the city input with the data that came from the server
        }
      });

	})
}

