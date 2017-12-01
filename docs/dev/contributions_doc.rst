*****************
How to Contribute
*****************
Contributing to CalPack can come in many forms including:

  * Testing
  * Documentation
  * Developing New Features and/or Fixing Known issues
  * Reporting Issues

Don't feel like you need a specific amount of experience to contribute.  Simply reporting an issue is contributing!  In order 
to develop *some* of the features within CalPack some knowledge of :code:`ctypes` is needed.

GitHub, Issue Tracking and Branching
====================================
Development of CalPack is done within `GitHub <https://github.com/KronoSKoderS/CalPack>`_.  Any issues that are encountered
or reported are tracked within GitHub's internal issues tracking.

When developing code we use the following 3 major branches:

    * :code:`prod` - production level code.  This is where relases are tracked.  It's from this version that the pypi repo is 
      updated.  Only :code:`integ` branch can be pushed to this branch.  This branch requires admin approval for Pull Requests
      to be merged.  
    * :code:`integ` - integration level code.  This is *nearly* a clone of :code:`prod`.  The :code:`dev` branch can push to this branch as well 
      any hotfixes (small critical changes that need to be deployed immediately.  
    * :code:`dev` - Main development happens here.  Any Pull Requests from developers should be against this branch.  

Any new Pull Request should be against the :code:`dev` branch.  When working on specific features, branch from the :code:`dev` branch
using the branch name :code:`feature/<feature-topic>`.  When a critical issue is identified that needs to be fixed immediately, branch
from the :code:`integ` branch using the branch name :code:`hotfix/<hotfix-topic>`

When we do releases, brances from the :code:`integ` branch will be done using the branch name :code:`v<version number>`.  

After each push into any branch a `Travis CI <https://travis-ci.org/KronoSKoderS/CalPack>`_ and 
`Appveyor <https://ci.appveyor.com/project/KronoSKoderS/calpack>`_ to run tests on differing python versions on linux and Windows.  
After successfully passing the unittests coverage results are uploaded to `coveralls <https://coveralls.io/github/KronoSKoderS/CalPack>`_ and 
`codacy <https://www.codacy.com/app/kronoskoders/CalPack>`_.  

.. warning:: Before a Pull Request into the :code:`prod` branch, all unittests and QA checks from Coveralls and Codacy have to pass first.  

Sprints and Sprint Planning
===========================

While issues are tracked within GitHub, we additionally use `ZenHub <https://app.zenhub.com/workspace/o/kronoskoders/calpack>`_
for prioritzing and planning future development of CalPack.  For instant message communication we use `slack <kronoskoders.slack.com>`_.  
To be invited to the channel send a message to :code:`superuser<dot>kronos<at>gmail<dot>com`.  

Sprints typically run for 2 weeks at a time.  


Developing code
===============

The best way to start developing is to look through the issues listed in the `issues <https://github.com/KronoSKoderS/CalPack/issues>`_ 
page of GitHub.  When creating new features or changes that affect the code, it's imperative that unittests are updated as well.  This
may require the creation of new unittests.  Any new tests that are implemented or old tests that have changed, need to go through a 
review with at least another CalPack developer.  

We try to use a TDD approach to development of new features.  Tests should be written **first** and then the features implemented.  
However this isn't always necessary.  If you decide to create a new feature or make changes to the code, please add any additional 
tests that will ensure the quality of the code you've created.  


Documentation
=============

Documentation is done using Sphinx and reStructured Text.  


Testing
=======

Even though developers should be creating unittests along with their code, additional testing may be required to ensure that the 
overal functionality is preserved.  Additional tests are always welcome so long as they provide value added to the testing of the
code.  Duplicate testing should be avoided and will be rejected during review if found.  

Next Topic - :doc:`tools_doc`