$(document).ready(function () {
        $('#wizard-one').show();
        $('#wizard-two').hide();
        $('#wizard-three').hide();
    })

    $('#wizard-one-forward').click(function () {
        $('#wizard-one').hide();
        $('#wizard-two').show();
        $('#wizard-three').hide();
    })

    $('#wizard-two-back').click(function () {
        $('#wizard-one').show();
        $('#wizard-two').hide();
        $('#wizard-three').hide();
    })

    $('#wizard-two-forward').click(function () {
        $('#wizard-one').hide();
        $('#wizard-two').hide();
        $('#wizard-three').show();
    })

    $('#wizard-three-back').click(function () {
        $('#wizard-one').hide();
        $('#wizard-two').show();
        $('#wizard-three').hide();
    })