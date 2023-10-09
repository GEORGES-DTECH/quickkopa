
importScripts('https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js');



workbox.routing.registerRoute(

   
    ({request}) => 
    
    request.destination === 'script',
   
    

     new workbox.strategies.StaleWhileRevalidate({
      "cacheName":"javascript",
       plugins: [
        new workbox.expiration.Plugin({
           maxEntries: 1000,
           maxAgeSeconds: 18000
          //  one day

         })
       ]
       })
    )

 
      workbox.routing.registerRoute(

        ({request}) => 
        request.destination === 'style',
    
         new workbox.strategies.StaleWhileRevalidate({
          "cacheName":"styles",
           plugins: [
            new workbox.expiration.Plugin({
               maxEntries: 1000,
               maxAgeSeconds: 18000
              //  one day
    
             })
           ]
           })
        )
     
         
   
   
workbox.routing.registerRoute(

  ({request}) => 
  request.destination === 'image',


  new workbox.strategies.CacheFirst({
   "cacheName":"images",
   plugins: [
    new workbox.expiration.Plugin({
      maxEntries: 1000,
      maxAgeSeconds:86400
      // one day
    })
  ]
   
   })
)


 




















