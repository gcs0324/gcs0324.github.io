(function(){
  var pages=[
    {href:'sc-01-arch.html',label:'01 架构总览'},
    {href:'sc-02-register.html',label:'02 注册中心'},
    {href:'sc-03-gateway.html',label:'03 网关&调用'},
    {href:'sc-04-reliability.html',label:'04 可靠性'},
    {href:'sc-05-interview.html',label:'05 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="sc-01-arch.html">Spring Cloud ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
