$(document).ready(()=>{
    $('.search-field').on('input',function(event){
        pattern = $(event.target).val().toLowerCase();
        if(pattern=='')
        {
            $('.searcheable-item').show();
        }else{
            $('.searcheable-item').each(function(index, value) {
                if($(this).find('.searchable-content').text().toLowerCase().includes(pattern)){
                    $(this).addClass('d-flex');
                    $(this).show();
                }
                else{
                    $(this).removeClass('d-flex');
                    $(this).hide();
                }
            });
        }
    });
});