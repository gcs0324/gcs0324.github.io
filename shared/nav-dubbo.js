(function(){
  var pages=[
    {href:'dubbo-outline.html',label:'导航'},
    {href:'dubbo-01-rpc.html',label:'01 RPC原理'},
    {href:'dubbo-02-arch.html',label:'02 Dubbo架构'},
    {href:'dubbo-03-registry.html',label:'03 注册中心'},
    {href:'dubbo-04-cluster.html',label:'04 集群容错'},
    {href:'dubbo-05-interview.html',label:'05 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="dubbo-outline.html">Dubbo ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
