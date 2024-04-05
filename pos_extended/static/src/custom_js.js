$(document).ready(function () {
    var isChecked = $('input[id="company"]:checked').val();
    $('input[name="company_type"]').change(function () {
        var isChecked = $('input[id="company"]:checked').val();
        if (isChecked === "company"){
            $('.hide_title').hide();
        }else{
            $('.hide_title').show();
        }
    });
});