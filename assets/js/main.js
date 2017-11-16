function testAnim(x) {
  $('#animationSandbox').removeClass().addClass(x + ' animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
    $(this).removeClass();
  });
};
$(document).ready(function(){
  $('.js--triggerAnimation').click(function(e){
    e.preventDefault();
    var anim = $('.js--animations').val();
    testAnim(anim);
  });
  $('.js--animations').change(function(){
    var anim = $(this).val();
    testAnim(anim);
  });
});
if ('addEventListener' in window) {
  window.addEventListener('load', function() { document.body.className = document.body.className.replace(/\bis-loading\b/, ''); });
  document.body.className += (navigator.userAgent.match(/(MSIE|rv:11\.0)/) ? ' is-ie' : '');
}
