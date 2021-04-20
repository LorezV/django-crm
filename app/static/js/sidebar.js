$(document).ready(function() {
    $('.burger_toggle').click(function() {
        $('#sidebar').toggleClass('expanded')
        $('.burger_toggle').toggleClass('expanded')
    })
})