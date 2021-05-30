$(document).ready(function(){
      $("#input").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#mytable tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });

$(document).ready(function (){
    var table = $('#table').DataTable({
       dom: 'lrtip',
        initComplete: function () {
          this.api().columns([1]).every( function () {
            var column = this;
            console.log(column);
            var select = $("#schoolfilter"); 
            column.data().unique().sort().each( function ( d, j ) {
              select.append( '<option value="'+d+'">'+d+'</option>' )
            } );
          } );
           this.api().columns([7]).every( function () {
            var column = this;
            console.log(column);
            var select = $("#age"); 
            column.data().unique().sort().each( function ( d, j ) {
              select.append( '<option value="'+d+'">'+d+'</option>' )
            } );
        } );
            
          $("#schoolfilter,#gender,#age,#ethnicityfilter,#continuing_New\
          ,#previoushoursfilter,#ethnicityinfo,#teachfilter,#promofilter,#socialfilter,\
          #hoursfilter, #gownfilter,#hatfilter,#statusfilter",).material_select();
       }
    });
    
    $('#schoolfilter').on('change', function(){
    	var search = [];
      
      $.each($('#schoolfilter option:selected'), function(){
      		search.push($(this).val());
      });
      
      search = search.join('|');
      table.column(1).search(search, true, false).draw();  
    });
    
    $('#age').on('change', function(){
    	var search = [];
      
      $.each($('#age option:selected'), function(){
      		search.push($(this).val());
      });
      
      search = search.join('|');
      table.column(7).search(search, true, false).draw();
    });

});

$(document).ready(function() {
    $('.selectpicker').click(function() {
        $("schoolfilter :selected").each(function() {
          return this.value
       }).map(function(){
          var $el = $(this);
          var value = $el.is('select') ? $el.find(':selected').text(): $el.val()
          return {
            col: $el.data('col'),
            value: value.toLowerCase()
          }
        });
    });
});
     $(document).ready(function () {
     var $rows = $('tbody#mytable tr')
     
     $(".table-filter").each(function(){
    var thisOptionValue=$(this).val();
      });
      var $filters = $('.selectpicker').change(function(){
       var filterArr = $filters.filter(function(){
          return this.value
       }).map(function(){
          var $el = $(this);
          var value = $el.is('select') ? $el.find(':selected').text(): $el.val()
          return {
            col: $el.data('col'),
            value: value.toLowerCase()
          }
       }).get();
       if(!filterArr.length){
         $rows.show()
       }else{
         $rows.hide().filter(function(){
            var $row = $(this)
            return filterArr.every(function(filterObj, i){
               var cellText = $row.find('td').eq(filterObj.col).text().toLowerCase();             
              return  cellText.includes(filterObj.value);
            })
         }).show()
       }
     })
    });