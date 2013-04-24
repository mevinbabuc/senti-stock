/* 
 *Author : Anenth
 */

var current = "none";
var loadmoreValue = 0;
var loadmoreButton =  jQuery('#loadmoreButton');


function get(url,table,loadMore)
{
    window.loadMore = loadMore;
    window.url = url;   
    if(url.indexOf("report") !== -1){
       
    }else{
        current = table ;
        window.content = jQuery("#"+ url + " tbody"); //Ajax data will be added here
        if(loadMore == 0){
            loadmoreValue = 0;
        }else
            loadmoreButton.button('loading');
        jQuery.ajax({
            type: "GET",
            url: url,
            data: {
                table : table ,
                lower : loadmoreValue
            },
            success: function(data) {
                loadmoreValue += 10;
                content_animate(data);
            }
        });
    }
}
function content_animate(data){
    var rightdiv = $("#rightContent");
   
    var easing = 'easeOutExpo';
    var duration =500;
    rightdiv.animate({
        left: '110%'
    }, duration,easing, function() {
        content.html(data);     //data added after the div hides
        rightdiv.animate({
            left: 0
        },duration,easing,function(){
            if(loadMore != 0)
                loadmoreButton.button('reset');
            //Button Bindings
            if(url.indexOf("sentiment") !== -1){
                jQuery('td.btn-group button').bind('click',function(){
                    button = jQuery(this);
                    cls = button.attr('id');
                    row = button.parent().parent();
                    id = button.parent().data('id');
                    change_sentiment(cls,id,row);  
                });
            }
            if(url.indexOf("classify") !== -1 ){
                jQuery('td button').bind('click',function(){
                    button = jQuery(this);
                    button.addClass('disabled').removeClass('btn-primary');
                    row = button.parent().parent();
                    tweet = row.children(':first-child').text();
                    classify(tweet,row);
                });
            }
        });
    });
}
function change_sentiment(val,id,row){
    jQuery.ajax({
        type: "GET",
        url: "changeSentiment", 
        data: {
            value : val, 
            id : id ,
            table : current
        },
        success: function(data){
            if(data == "true")
                row.fadeOut(500);
            else
                alert("Some problem");
        }
    });
}
function classify(data,row){
    jQuery.ajax({
        type: "GET",
        url: "classify_data", 
        data: {
            tweet : data,
            table : current
        },
        success: function(data){
            if(data){
                polarity = row.children(':nth-child(2)').find('span');
                polarity.addClass(data).text(data);
                if(data =="negative")
                    polarity.parent().parent().addClass("warning")
                else
                    polarity.parent().parent().addClass("success")
            }
            else
                alert("Some problem");
        }
    });
}
           
           
// Add new data
function newdata(url){
    setInterval(function(){
        if(url  )
            jQuery.ajax({
                type: "GET",
                url: 'newDataRejuest',
                data: {
                    url : url
                },
                success: function(data) {
                    content.html(data).hide().fadeIn(500); //DATA ADDED
                }
            });
    },5000); 
}

function settings(type){
    $.ajax({
        type:"GET",
        url:"settings",
        data:{
            type : type
        },
        success: function(data){
            alert(data);
        }
    });
}
//  Navigation
               
var main_nav=
'<li class="nav-header">Collected Data</li>' +
'<li>                <a href="#news"                                         data-toggle="tab"><i class="icon-globe">         </i> News</a></li>'+
'<li>                <a href="#qoutes"                                       data-toggle="tab"><i class="icon-indent-right">  </i> Stock Quotes</a></li>'+
'<li>                <a href="#sentiment"                                    data-toggle="tab"><i class="icon-comment">       </i> User Sentiments</a></li>'+
'<li class="nav-header">Actions</li>'+
'<li>                <a href="#classify"                                     data-toggle="tab"><i class="icon-align-center">  </i> Classify</a></li>'+
'<li class="nav-header">The Public</li>'+
'<li>                <a href="./"                                                      ><i class="icon-briefcase">     </i> Public Page</a></li>'+
'<li class="nav-header">Control Panel</li>'+
'<li>                <a href="#setting"                                      data-toggle="tab"><i class="icon-wrench">     </i> Setting</a></li>';
   
var go_back_link = '<li>  <a onclick="load()" href="#" ><i class="icon-arrow-left">     </i> Go Back</a></li>';

function nav_elements(table,header){
    return '<li class="nav-header">'+header+'</li>' +
    '<li><a href="#'+table+'_apple"          onclick="get(\''+table+'\',\'aapl\',0)"         data-toggle="tab"><i class="icon-font">          </i> Apple [$APPL]</a></li>'+
    '<li><a href="#'+table+'_google"         onclick="get(\''+table+'\',\'goog\',0)"         data-toggle="tab"><i class="icon-search">          </i> Google [$GOOG]</a></li>'+
    '<li><a href="#'+table+'_bac"            onclick="get(\''+table+'\',\'bac\',0)"          data-toggle="tab"><i class="icon-bold">          </i> Bank Of America [$BAC]</a></li>' + go_back_link;
}
var setting_nav =
'<div class="settings"> ' +
'<li class="nav-header">Settings</li>' +
'<li><a href="#dataCollector"  ><i class="icon-chevron-right">           </i> Data Collector</a></li>'+
'<li><a href="#training"       ><i class="icon-chevron-right">           </i> Training</a></li>  '+ 
'<li><a href="#newsQuotes"     ><i class="icon-chevron-right">           </i> News & Quotes</a></li>' +
'<li><a href="#linearReg"      ><i class="icon-signal">                  </i> Linear Regression</a></li>' +
'</div>'+go_back_link;

var nav= $('#main-nav');

  
function nav_animate(data,bind){
    easing = 'easeInOutBack';
    duration =500;
    nav.animate({
        left: -250
    }, duration,easing, function() {
        nav.html(data)  //data added to the dom
        .animate({
            left:10
        },duration,easing,function(){
            if(bind == 1)
                bind_main_nav_a();  // buttons binded !
        });
    });
         
}

function bind_main_nav_a(){           
    nav.find("a").on('click',function(){
        current_nav = $(this).attr('href');
        if(current_nav.indexOf("news") !== -1 ){
            nav_animate(nav_elements('news','News Collected'));
        }else if(current_nav.indexOf("sentiment") !== -1 ){
            nav_animate(nav_elements('sentiment','Sentiment Collected'));
        }else if(current_nav.indexOf("qoutes") !== -1 ){
            nav_animate(nav_elements('qoutes','Stock Quotes'));
        }else if(current_nav.indexOf("classify") !== -1 ){
            nav_animate(nav_elements('classify','Classify'));
        }else if(current_nav.indexOf("report") !== -1 ){
            nav_animate(nav_elements('report','Report'));
        }else if(current_nav.indexOf("setting") !== -1 ){
            nav_animate(setting_nav);
            $('#settings').show();
        }
    });
}
function load(){
    nav_animate(main_nav,1); 
    $(".active").removeClass('active');
}


window.onload = load;