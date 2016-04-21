#!/usr/bin/python

import os
import sys

def bash_execute(bash_cmd):
	os.system(bash_cmd)

if __name__ == '__main__':
	insdc_number = sys.argv[1:]

	#create a working directory
	#then create 6 directories inside
	if os.path.isdir('cmgbiotools_result'):
		bash_execute('rm -r cmgbiotools_result')

	bash_execute('mkdir cmgbiotools_result')
	os.chdir('./cmgbiotools_result')

	bash_execute('mkdir gbk dna fsa fna stats codon_usage')

	#download genbank files from NCBI to gbk folder
	os.chdir('./gbk')
	for insdc in insdc_number:
		command_line = 'gbk_get -a ' +insdc+ ' > ' +insdc+ '.gbk'
		bash_execute(command_line)

	#extract name of organisms
	for insdc in insdc_number:
		command_line = 'gbk_ExtractName ' +insdc+ '.gbk'
		bash_execute(command_line)

	#move isndc.gbk to an isndc folder
	bash_execute('mkdir isndc_gbk')
	for insdc in insdc_number:
		command_line = 'mv ' +insdc+ '.gbk isndc_gbk'
		bash_execute(command_line)

	#extract dna from gbk files and move them to a dna folder
	gbk_files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for gbk in gbk_files:
		command_line = 'saco_convert -I genbank -O fasta ' +gbk+ ' > ' +gbk+ '.dna'
		bash_execute(command_line)

	for gbk in gbk_files:
		command_line = 'mv ' +gbk+ '.dna ../dna'
		bash_execute(command_line)

	#extract genes and proteins
	for gbk in gbk_files:
		command_line = 'gbk_ExtractGeneProt ' + gbk
		bash_execute(command_line)

	#move genes and proteins to fsa and fna folders
	for gbk in gbk_files:
		command_line = 'mv ' +gbk+ '.fna ../fna'
		bash_execute(command_line)

	for gbk in gbk_files:
		command_line = 'mv ' +gbk+ '.fsa ../fsa'
		bash_execute(command_line)

	#calculate basisc statistics
	os.chdir('../dna')
	dna_files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for dna in dna_files:
		command_line = 'stats_genomeDNA ' +dna+ ' >> genomeStats.all'
		bash_execute(command_line)

	#move basic statistics to a stats folder
	command_line = 'mv genomeStats.all ../stats'
	bash_execute(command_line)

	#copy dna files to codon_usage directory and calculate codon usage
	os.chdir('../codon_usage')
	bash_execute('cp ../fna/*.fna .')

	#copy scripts for calculating codonUsage
	bash_execute('cp ../../lib/comp_CodonAaUsage_codonUsage.sh .')
	bash_execute('cp ../../lib/aaUsage.r .')
	bash_execute('cp ../../lib/codonUsage.r .')

	#calculate amino acid and codon usage
	fna_files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for fna in fna_files:
		if fna.endswith(".fna"):
			command_line = 'stats_usage ' +fna+ ' /usr/bin/gnuplot'
			bash_execute(command_line)

	bash_execute('./comp_CodonAaUsage_codonUsage.sh')

	#compare codon_usage heat-map
	bash_execute('R -f codonUsage.r')
	bash_execute('mv Rplots.pdf codonUsage.pdf')

	#compare amino_acid_usage heat-map
	bash_execute('R -f aaUsage.r')
	bash_execute('mv Rplots.pdf aaUsage.pdf')



	# command=' '.join(x[1:])
	# y = 'for x in '+command+';do echo $x;done'
	# bash_execute(y)

# os.system('for x in '+command+';do echo $x;done')
