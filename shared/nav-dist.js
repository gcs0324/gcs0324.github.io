(function(){
  var pages=[
    {href:'dist-outline.html',label:'导航'},
    {href:'dist-01-theory.html',label:'01 理论基础'},
    {href:'dist-02-transaction.html',label:'02 分布式事务'},
    {href:'dist-03-lock-id.html',label:'03 锁 & ID'},
    {href:'dist-04-interview.html',label:'04 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="dist-outline.html">分布式 ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
