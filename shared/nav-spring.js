(function(){
  var pages=[
    {href:'spring-outline.html',label:'导航'},
    {href:'spring-01-ioc.html',label:'01 IoC/DI'},
    {href:'spring-02-aop.html',label:'02 AOP'},
    {href:'spring-03-tx.html',label:'03 事务'},
    {href:'spring-04-mvc.html',label:'04 MVC'},
    {href:'spring-05-boot.html',label:'05 Boot'},
    {href:'spring-06-interview.html',label:'06 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="spring-outline.html">Spring ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
