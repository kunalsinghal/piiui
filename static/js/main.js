
function init() {
    window.Counter = 0;
    window.arr = [];
}
function pop(x){

    var s = x.toString();
    elem = document.getElementById(s);

    if (elem.className == "words"){
	   elem.className = "words high";
    	window.Counter += 1;
        window.arr.push(x);
    }
    else{
    	elem.className = "words";
    	window.Counter -= 1;
        window.arr.splice(window.arr.indexOf(x), 1);
    }
    changeRules();
}
function changeRules() {
    var str = "[" + arr.toString() + "]";
    $.ajax({
        type: "POST",
        url: "back",
        data: {arr: str},

    }).done(function(data){
        var temp = JSON.parse(data);
        temp = JSON.parse(temp.arr);
        var h = "" ;

        for(var i = 0; i < temp.length; i ++){
            h = h + "<tr class='row'>";

            for(var j = 0; j < temp[i].length; j++){
                var id = temp[i][j] + "-" + temp[i][0] + "-" + i.toString();
                h = h + "<td class='options' data-root='"+temp[i][0]+"' + id='"+id+"' onclick=\"opted('"+id+"')\">" + temp[i][j] + "</td>";
            }
            h = h + "</tr>";
        }

        $('#rules').html(h);
    });
}
function opted(str){
    str = '#' + str;
    $(str).toggleClass('high');
}
function recordRule(){
    var lis = [];
    var roots = [];
    $('.options.high').each(function(){
        lis[lis.length] = $(this).html();
        roots[roots.length] = $(this).attr('data-root');
    });
    $.ajax({
        type: "POST",
        url: "nextrule",
        data: {words: lis.toString(), base: roots.toString()},
    });
    window.Counter = 0;
    window.arr = []
    $('.high').removeClass('high');
    changeRules();
}
$(document).ready(function(){
    $('#nextrule').click(function(){
        recordRule();
    });
});
