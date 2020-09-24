<!--
    index.php = Callisto main index file
-->

<?php include_once "headers.inc" ?>
<?php include_once "menu.inc" ?>
  <!-- Start search box -->
  <div id="mu-search">
    <div class="mu-search-area">      
      <button class="mu-search-close"><span class="fa fa-close"></span></button>
      <div class="container">
        <div class="row">
          <div class="col-md-12">            
            <form class="mu-search-form">
              <input type="search" placeholder="Type Your Keyword(s) & Hit Enter">              
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- End search box -->
  <!-- Start Slider -->
  <section id="mu-slider">
    <!-- Start single slider item -->
    <div class="mu-slider-single">
      <div class="mu-slider-img">
        <figure>
          <img src="assets/img/slider/bandeau.jpg" alt="img">
        </figure>
      </div>
      <div class="mu-slider-content">
        
        <span></span>
        <h2>Welcome to CALLISTO</h2>
        <p></p>
        <!-- <a href="#" class="mu-read-more-btn">Read More</a>-->
      </div>
    </div>
    <!-- Start single slider item -->    
  </section>
  <!-- End Slider -->
  <!-- Start service  -->
  <section id="mu-service">
    <div class="container">
      <div class="row">
        <div class="col-lg-12 col-md-12">
          <div class="mu-service-area">
            <!-- Start single service -->
            <div class="mu-service-single">
              <span class="fa fa-users"></span>
              <h3>Collaborate</h3>
              <p>Use the CALLISTO DataVerse instance to share your data, and discover other datasets useful for you.</p>
	      <!-- <a href="https://callisto.calmip.univ-toulouse.fr/loginpage.xhtml" target="_blank" class="mu-read-more-btn">Begin</a> -->
	      <?php if ($logged==true): ?>
	      <a href="/index-dataverse.php" target="_blank" class="mu-read-more-btn">Begin</a>
	      <?php else: ?>
	      <a href="/Shibboleth.sso/Login?target=/index-dataverse.php" target="_blank" class="mu-read-more-btn">Begin</a>
              <?php endif ?>
            </div>
            <!-- Start single service -->
            <!-- Start single service -->
            <div class="mu-service-single">
              <span class="fa fa-table"></span>
              <h3>Work</h3>
              <p>Use the embedded tools to ease the discovery of data and software. Tell CALLISTO what you need and let us guide you!</p>
	       <a href="work.html" class="mu-read-more-btn">Web interface</a>
	       <!-- <a href="http://callisto-local.mylaptop/hub/" class="mu-read-more-btn">Interactive scripting</a> -->
            </div>
            <!-- Start single service -->
	    <div class="mu-service-single">
              <span class="fa fa-table"></span>
              <h3>Toolbox</h3>
              <p>Find online tools that may help you describing your data, understanding the interoperability whereabouts, writing your DMPs and more...</p>
	             <a href="tools.html" class="mu-read-more-btn">Go</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <!-- End service  -->

  <!-- Start about us -->
  <section id="mu-about-us">
    <div class="container">
      <!-- Start Title -->
      <div class="mu-title">
        <h2>About Callisto</h2>              
      </div>
      <!-- End Title -->
      <p>CALmip Launches an Interface for a Semantic Toolbox Online (CALLISTO) is a Web interface allowing researchers to share, discover and use data, data services and analysis services. It is intended to help collaborators achieve a FAIR (Findable, Accessible, Interoperable and Reliable) data management. <br/> <br/>Callisto is a work in progress. Its intent is to provide tools and methods for ensuring FAIR access to scientific data for the CALMIP community of users.</p>
         
  </section>
  <!-- End about us -->
  </body>
</html>


