document.getElementById('botton_img').addEventListener('click', function(){
    window.location.href('{% url "movies" %}')
})