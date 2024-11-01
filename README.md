<h1>ChE-411: Project</h1>

<h2>Introduction 🌟</h2>
<p>This project aims to reproduce results from the paper <strong>"A detailed genome-scale metabolic model of <em>Clostridium thermocellum</em> investigates sources of pyrophosphate for driving glycolysis"</strong>.</p>

<h2>Informations 📋</h2>
<p>The paper on which this project is based on can be found <a href="Paper.pdf">here</a>. No report is expected, only a PowerPoint presentation.
<p>The metabolic models the authors proposed are publicly available through the Maranas Group's <a href="https://github.com/maranasgroup/iCTH669">GitHub repository</a>.
<p>The models to use are in fact the models <i>iCTH670_w_GLGC</i> and <i>iCTH670_wo_GLGC</i> in the authors' GitHub repository. For clarity, they have been renamed to <i>iCTH669_w_GLGC</i> and <i>iCTH669_wo_GLGC</i> in this repository, in the <a href="Models">Models</a> folder.</p>

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
    <td>Redesign PowerPoint presentation</td>
    <td align="center">Everyone</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Reproduce <b>Figure 2 a)</b> and <b>Figure 2 b)</b> using the method described in the paper</td>
    <td align="center">Marija</td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td>Reproduce <b>Figure 2</b> by minimizing cellobiose uptake for a given ethanol yield</td>
    <td align="center">César</td>
    <td align="center">[ ]</td>
  </tr>
  <tr>
    <td>Reproduce <b>Table 2</b></td>
    <td align="center">Jonathan</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Understand how to obtain <b>Table 3</b></td>
    <td align="center">Tom</td>
    <td align="center">[x]</td>
  </tr>
  <tr>
    <td>Bonus: Reproduce <b>Table 3</b></td>
    <td align="center">Tom</td>
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
<p>Contains all results generated for this project, with each member having its own folder for clarity.</p>

<h3>Scripts</h3>
<p>Contains all the scripts used in this project:</p>
<p><b>generate_memote_reports.py:</b> python script to generate the MEMOTE reports of the models contained in the <i>Models</i> folder.</p>
