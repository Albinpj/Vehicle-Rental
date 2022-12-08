odoo.define('vechile_rental.online_rent_request_form',function(require){
    "use strict";

    var ajax = require('web.ajax');
    $(function(){
        $('#period_type').on('change',function(){
            var period_name = $("select[name ='period_type']").val();
            var vehicle_name = $("select[name ='vehicle_id']").val();
            console.log("kk",vehicle_name, period_name)
            ajax.jsonRpc('/get_period','call',{
                'period':period_name,
                'vehicles':vehicle_name
            }).then(function(response){
                    $('#amt').val(response['rent_amount']);
             });
        });
    });
})

