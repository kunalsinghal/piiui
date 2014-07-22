/// inititalizes global variables
function init() {
    /// Counter is the number of words highlighted
    window.Counter = 0;
    /// arr is contains the list of indices of words which are highlighted
    window.arr = [];
}

/// toggles highlighting and change global variables accordingly
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

/// connects with backend using ajax then generates rule options
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

        /// this loop creates rows of table of rules (for different highlighted words)
        for(var i = 0; i < temp.length; i ++){
            h = h + "<tr class='row'>";
            /// this table creates table divisions in the table (for options)
            for(var j = 0; j < temp[i].length; j++){
                var id = temp[i][j] + "-" + temp[i][0] + "-" + i.toString();
                /// data-root is the root string of the option
                h = h + "<td class='options' data-root='"+temp[i][0]+"' + id='"+id+"' onclick=\"opted('"+id+"')\">" + temp[i][j] + "</td>";
            }
            h = h + "</tr>";
        }

        $('#rules').html(h);
    });
}


/// this function is called when a rule option is clicked and it toggles the highlighting for that option
function opted(str){
    str = '#' + str;
    $(str).toggleClass('high');
}

function recordRule(){
    /// list of rule elements
    var lis = [];
    /// contains root string of each rule element
    var roots = [];
    /// for each highlighted rule element, it adds the element and root word in lists
    $('.options.high').each(function(){
        lis[lis.length] = $(this).html();
        roots[roots.length] = $(this).attr('data-root');
    });
    /// send the data to backend
    $.ajax({
        type: "POST",
        url: "nextrule",
        data: {words: lis.toString(), base: roots.toString()},
    });
    /// reset global variables
    window.Counter = 0;
    window.arr = []
    /// reset highlighting
    $('.high').removeClass('high');
    changeRules();
}
function changeTweet(){
    /// ping backend for new tweet
    $.ajax({
        type: "POST",
        url: "nexttweet"
    }).done(function(data){
        console.log(data);
        $('#tweet').html(data);
    });
}

$(document).ready(function(){
    $('#nextrule').click(function(){
        recordRule();
    });
    $('#nexttweet').click(function(){
        recordRule();
        changeTweet();
    });
});
