
var page ="store";
function fetch(a) {    
var id = document.getElementsByClassName("btn active")[0].value;

console.log(page);
var reqData = {'url':a,'val':id,'page':page};
  $.ajax({

type:"POST",
contentType: "application/json; charset=utf-8",
dataType: "json",
data: JSON.stringify(reqData),
url: "http://127.0.0.1:5000/url",
success: function(data){
console.log(data[0]['url']);
// end of forEach
document.getElementById('urlvalue').innerHTML = 'Hi, I am Arun Banik';
window.localStorage.setItem('response', data);
window.location.href = "http://127.0.0.1:5000/user";



}
})
 
}

function clearValue(){
    
 document.getElementById("masterUrl").value = "";

}
function store(pagevalue){

    window.page = pagevalue;
//document.getElementById("toggle").value = result;
}

$(document).ready(function(){
$('#search').attr('disabled',true);

$('#masterUrl').keyup(function(){
    if($(this).val().length !=0){
        $('#search').attr('disabled', false);
    }
    else
    {
        $('#search').attr('disabled', true);        
    }
})

});

var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
btns[i].addEventListener("click", function(){
var current = document.getElementsByClassName("active");
current[0].className = current[0].className.replace(" active", "");
this.className += " active";
 console.log(this.className);
});

}





$(document).ready(function() {
$("#search").click(function() {
$(this).text( ($(this).text() == 'Go' ? 'Stop' : 'Go') )
if($(this).text() == 'Stop'){
 $(this).css('background-color', 'white');
 $(this).css('color', 'red');
 $(this).css("border-color", 'red');

}
else{
    $(this).css('background-color', 'dodgerblue');
 $(this).css('color', 'black');
 $(this).css("border-color", 'black');
}
})
})


$(document).ready(function(){
var option="stroree";
$(".link").addClass("color");
//   First active item

$(".menu--item__one").click(function(){
 $(".bottom__line").addClass("bottom__active");
 $(".link").addClass("color");
 $(".link1").removeClass("color1");
 $(".link2").removeClass("color2");
 $(".bottom__line").removeClass("bottom__active1 bottom__active2");
option="store";
});

//  Second active item
$(".menu--item__two").click(function(){
  $(".bottom__line").addClass("bottom__active1");
  $(".link1").addClass("color1");
  $(".link").removeClass("color");
  $(".link2").removeClass("color2");
  $(".bottom__line").removeClass("bottom__active bottom__active2");
option = "Marketing";
});

console.log(option);



});


