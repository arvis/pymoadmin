$(function(){ 
    $.get("/dblist", function(data){
        var table_data=JSON.parse(data);
        for (i in table_data){
            $("#db_list").append("<option value="+table_data[i]+"> "+table_data[i]+"</option>" )
            }
        });

    $("#db_list").change( function() {
        $.get("/tablelist/"+$("#db_list").val(), function(data){
        	//$('#table_list').empty();
			$('#table_list').find('option').remove();
            var table_data=JSON.parse(data);
            for (i in table_data){
                $("#table_list").append("<option value="+table_data[i]+"> "+table_data[i]+"</option>" );
            }
        });
    });

    $("#table_list").change( function() {
        $.get("/get_all/"+$("#table_list").val(), function(data){
            $("#table_data").html(data);
        });
    });

});

