<h1>ChE-411: Project</h1>

<h2>Introduction 🌟</h2>
<p>This project aims to reproduce results from the paper <strong>"A detailed genome-scale metabolic model of <em>Clostridium thermocellum</em> investigates sources of pyrophosphate for driving glycolysis"</strong>.</p>

<h2>Informations 📋</h2>
<p>The paper on which this project is based on can be found <a href="Paper.pdf">here</a>. No report is expected, only a PowerPoint presentation.
<p>The metabolic models the authors proposed are publicly available through the Maranas Group's <a href="https://github.com/maranasgroup/iCTH669">GitHub repository</a>.

<h2>Tasks 🛠️ (Updated Every Thursday)</h2>

<h3>Week 5 (October 11th, 2024)</h3>

<table>
  <tr>
    <th width="1500"; align="left">Task</th>
    <th width="250">Person</th>
    <th width="250"">Status</th>
  </tr>
  <tr>
    <td>Read the paper</td>
    <td align="center">Everyone</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Explore the GitHub code</td>
    <td align="center">Everyone</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Make a presentation for the TA summarizing the paper and the analyses that need to be done</td>
    <td align="center">Everyone</td>
    <td align="center">[x]</td>
  </tr>
</table>

<h3>Week 7 (November 1st, 2024)</h3>

<table>
  <tr>
    <th width="1500"; align="left">Task</th>
    <th width="250">Person</th>
    <th width="250">Status</th>
  </tr>
  <tr>
    <td><a href="Paper review.pptx">Redesign PowerPoint presentation</a></td>
    <td align="center">Everyone</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Reproduce <b>Figure 2 a)</b> and <b>Figure 2 b)</b> (with other metabolites like lactate) using the method described in the paper</td>
    <td align="center">Marija/Jonathan</td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td>Reproduce <b>Figure 2</b> by minimizing cellobiose uptake for a given ethanol yield (optional)</td>
    <td align="center">César</td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td><a href="Results/Jonathan/Table 2.xlsx">Reproduce <b>Table 2</b></a></td>
    <td align="center">Jonathan</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td><a href="Results/Tom/Table 3 results.docx">Understand how to obtain <b>Table 3</b></a></td>
    <td align="center">Tom</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Bonus: Reproduce <b>Table 3</b></td>
    <td align="center">Tom</td>
    <td align="center">[ ]</td>
  </tr>
</table>

<h3>Week 8 (November 5th, 2024)</h3>

<table>
  <tr>
    <th width="1500"; align="left">Task</th>
    <th width="250">Person</th>
    <th width="250">Status</th>
  <tr>
    <td>Reproduce plot for <b>Figure 3</b></td>
    <td align="center">Jonathan</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Understand <b>Table 4</b></td>
    <td align="center"></td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td>Discuss what was intersting, what can we do more with the model...</td>
    <td align="center">Everyone</td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td>Redo the presentation to include more biological background</td>
    <td align="center">Everyone</td>
    <td align="center">[ ]</td>
  </tr>
</table>


<p>Additional tasks will be added each week based on progress and new insights.</p>

<h2>Content of this repository 📂</h2>
<h3>.Archives</h3>
<p>Contains old files, such as previous presentation or unused models and memote reports, only use as a tracking purpose.</p>

<h3>Models</h3>
<p>Contains the metabolism models <i>iCBI665</i> and <i>iCTH669</i> as .sbml files, with and without GlgC (Glucose-1-phosphate adenylyltransferase).</p>

<h3>Reports</h3>
<p>Contains the MEMOTE reports for the <i>iCBI665</i> and <i>iCTH669</i>.</p>

<h3>Results</h3>
<p>Contains all results generated for this project.</p>

<h3>Scripts</h3>
<p>Contains all the scripts used in this project:</p>

<p><a href="Scripts\Biomass yields"><b>biomass_yield_<<i>strain></i>.py</b></a> python scripts to calculate the maximum biomass flux and yield for each strain. For this script to work, the python package <i>cobra</i> must by installed via <ip>pip install cobra</ip> and be sure to have the models <i>iCTH669</i> with and without GlgC.</p>

<p><a href="Scripts\PPi reactions"><b>calc_n_ppi_reactions.py</b></a> python scripts to report the numbers of producing or consuming PP<sub>i</sub> reactions for each strain, and to calculate their maximum and minimum PP<sub>i</sub> flux and production with FBA.</p>

<p><a href="Scripts\PPi reactions"><b>plot_ppi_producers.py</b></a> python scripts to plot the number of low, medium and high PP<sub>i</sub> producing reactions found with <a href="Scripts\PPi reactions"><b>calc_n_ppi_reactions.py</b></a>.</p>

<p><a href="Scripts\MEMOTE reports"><b>generate_memote_reports.py:</b></a> python script to generate the MEMOTE reports of the models contained in the <i>Models</i> folder. For this script to work, the python package <i>memote</i> must be installed via <i>pip install memote</i>.</p>
