
$.fn.dataTable.Api.register( 'column().data().sum()', function () {
  return this.reduce( function (a, b) {
      var x = parseFloat( a ) || 0;
      var y = parseFloat( b ) || 0;
      return x + y;
  } );
} );
 
 $(document).ready(function () {
    var table = $('#table').DataTable({ 
      "sPaginationType": "full_numbers",
      initComplete: function () {
        count = 0;
        this.api().columns().every(function () {
          var title = this.header();
          //replace spaces with dashes
          title = $(title).html().replace(/[\W]/g, '-');
          var column = this;
          var select = $('<select id="' + title + '" class="select2" ></select>')
            .appendTo($(column.footer()).empty())
            .on('change', function () {
              //Get the "text" property from each selected data 
              //regex escape the value and store in array
              var data = $.map($(this).select2('data'), function (value, key) {
                return value.text ? '^' + $.fn.dataTable.util.escapeRegex(value.text) + '$' : null;
              });

              //if no data selected use ""
              if (data.length === 0) {
                data = [""];
              }

              //join array into string with regex or (|)
              var val = data.join('|');

              //search for the option(s) selected
              column
                .search(val ? val : '', true, false)
                .draw();
            });

          column.data().unique().sort().each(function (d, j) {
            select.append('<option value="' + d + '">' + d + '</option>');
          });

          //use column title as selector and placeholder
          $('#' + title).select2({
            multiple: true,
            closeOnSelect: false,
            placeholder: "Please Select"
          });

          //initially clear select otherwise first option is selected
          $('.select2').val(null).trigger('change');

        });
      }
    });
  });

  $(document).ready(function () {
    $('#table').on('click','.clickable',function () {
      window.document.location = $(this).data("href");
      });
    });
 
