(function() {
  var base = 'https://shawnma.com/app/cert';
  var TEXT_PROP = 'yourtext';
  window.OCS = {
    preview : function(pid) {
      console.log("preview " + pid);
      $("#ProductPhotoImg").attr('src', base + '/preview/' + pid + '/' + encodeURIComponent($("#" + TEXT_PROP).val()));
    }
  };
  var main_script = function($) {
      // we are on checkout page
      console.log("trying to fetch " + Shopify.checkout.order_id);
      var line_items = Shopify.checkout.line_items;
      order = Shopify.checkout.order_id;
      var found = false;
      var html = '<div id="OCS_outer"><h1>Download your certificates</h1><div>';
      for (var i in line_items) {
          var item = line_items[i];
          var p = item['properties'];
          if (p && p[TEXT_PROP]) {
              // TODO: what if user didn't input anything?
              found = true;
              html  += '<li><a href="' + base + '/download/' + order + '/' + i + '">Download item ' + (parseInt(i)+1) + '</a></li>';
          }
      }
      if (found) {
          html += '</ul></div>';
          Shopify.Checkout.OrderStatus.addContentBox($(html));
      }
  }
  var load_script = function(url, callback) {
    var script = document.createElement("script")
    script.type = "text/javascript";
 
    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
                    script.readyState == "complete"){
                script.onreadystatechange = null;
                callback(jQuery);
            }
        };
    } else {  //Others
        script.onload = function(){
            callback(jQuery);
        };
    }
 
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
  }
  var path = window.location.pathname.split('/');
  if (path[2] === 'checkouts' && path[4] === 'thank_you') {
    if ((typeof jQuery === 'undefined') || (parseFloat(jQuery.fn.jquery) < 1.7)) {
        load_script('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', main_script);
    } else {
        main_script(jQuery);
    }
  }
})();
