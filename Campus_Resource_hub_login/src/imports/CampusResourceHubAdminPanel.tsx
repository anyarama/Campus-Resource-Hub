import svgPaths from "./svg-dmqc24sl3e";

function Section() {
  return (
    <div className="h-[1874px] relative shrink-0 w-0" data-name="Section">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[1874px] w-0" />
    </div>
  );
}

function Heading() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="Heading 1">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">Dashboard</p>
    </div>
  );
}

function Paragraph() {
  return (
    <div className="h-[24px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[24px] left-0 not-italic text-[#6e6e6e] text-[15px] text-nowrap top-0 whitespace-pre">{`Welcome back! Here's what's happening with your campus resources.`}</p>
    </div>
  );
}

function Container() {
  return (
    <div className="h-[72px] relative shrink-0 w-[493.961px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[8px] h-[72px] items-start relative w-[493.961px]">
        <Heading />
        <Paragraph />
      </div>
    </div>
  );
}

function ChButton() {
  return (
    <div className="bg-[#fbfaf9] h-[36px] relative rounded-[8px] shrink-0 w-[124.258px]" data-name="CHButton">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[36px] items-center justify-center px-[17px] py-px relative w-[124.258px]">
        <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#990000] text-[13px] text-nowrap whitespace-pre">View Calendar</p>
      </div>
    </div>
  );
}

function Icon() {
  return (
    <div className="absolute left-[16px] size-[16px] top-[10px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M5.33333 1.33333V4" id="Vector" stroke="var(--stroke-0, white)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M10.6667 1.33333V4" id="Vector_2" stroke="var(--stroke-0, white)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p3ee34580} id="Vector_3" stroke="var(--stroke-0, white)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M2 6.66667H14" id="Vector_4" stroke="var(--stroke-0, white)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function ChButton1() {
  return (
    <div className="basis-0 bg-[#990000] grow h-[36px] min-h-px min-w-px relative rounded-[8px] shrink-0" data-name="CHButton">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[36px] relative w-full">
        <Icon />
        <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-[40px] not-italic text-[13px] text-nowrap text-white top-[9px] whitespace-pre">New Booking</p>
      </div>
    </div>
  );
}

function Container1() {
  return (
    <div className="h-[36px] relative shrink-0 w-[274.18px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[36px] items-start relative w-[274.18px]">
        <ChButton />
        <ChButton1 />
      </div>
    </div>
  );
}

function Header() {
  return (
    <div className="h-[72px] relative shrink-0 w-[1015px]" data-name="Header">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[72px] items-center justify-between relative w-[1015px]">
        <Container />
        <Container1 />
      </div>
    </div>
  );
}

function Icon1() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d="M6.66667 1.66667V5" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d="M13.3333 1.66667V5" id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p1da67b80} id="Vector_3" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d="M2.5 8.33333H17.5" id="Vector_4" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Container2() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon1 />
    </div>
  );
}

function Text() {
  return (
    <div className="absolute h-[36px] left-[50px] top-[4px] w-[87.75px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] top-0 w-[57px]">Total Bookings</p>
    </div>
  );
}

function Container3() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[137.75px]" data-name="Container">
      <Container2 />
      <Text />
    </div>
  );
}

function Icon2() {
  return (
    <div className="h-[24px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 48 22">
          <path d={svgPaths.p2f947200} fill="var(--fill-0, #990000)" id="Vector" opacity="0.08" />
        </svg>
      </div>
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <div className="absolute inset-[-3.41%_-1.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 50 24">
            <path d={svgPaths.p15394900} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[-4.17%_-2%_87.5%_94%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 4 4">
          <path d={svgPaths.p12ed5580} fill="var(--fill-0, #990000)" id="Vector" />
        </svg>
      </div>
    </div>
  );
}

function Container4() {
  return (
    <div className="absolute content-stretch flex flex-col h-[24px] items-start left-[149.75px] top-[4px] w-[50px]" data-name="Container">
      <Icon2 />
    </div>
  );
}

function ChStatCard() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container3 />
      <Container4 />
    </div>
  );
}

function ChStatCard1() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">1,284</p>
    </div>
  );
}

function Icon3() {
  return (
    <div className="relative shrink-0 size-[12px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12 12">
        <g id="Icon">
          <path d="M2.5 6L6 2.5L9.5 6" id="Vector" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
          <path d="M6 9.5V2.5" id="Vector_2" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
        </g>
      </svg>
    </div>
  );
}

function Text1() {
  return (
    <div className="basis-0 grow h-[16px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[16px] relative w-full">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] left-0 not-italic text-[#1b5e20] text-[12px] text-nowrap top-[0.5px] whitespace-pre">+8%</p>
      </div>
    </div>
  );
}

function ChStatCard2() {
  return (
    <div className="h-[16px] relative shrink-0 w-[41.953px]" data-name="CHStatCard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[16px] items-center relative w-[41.953px]">
        <Icon3 />
        <Text1 />
      </div>
    </div>
  );
}

function ChBadge() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[59.953px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center p-px relative w-[59.953px]">
        <ChStatCard2 />
      </div>
    </div>
  );
}

function Text2() {
  return (
    <div className="h-[18px] relative shrink-0 w-[82.508px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[82.508px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">vs last month</p>
      </div>
    </div>
  );
}

function ChStatCard3() {
  return (
    <div className="content-stretch flex gap-[8px] h-[26px] items-center relative shrink-0 w-full" data-name="CHStatCard">
      <ChBadge />
      <Text2 />
    </div>
  );
}

function Container5() {
  return (
    <div className="[grid-area:1_/_1] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard />
          <ChStatCard1 />
          <ChStatCard3 />
        </div>
      </div>
    </div>
  );
}

function Icon4() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d={svgPaths.p25397b80} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p18406864} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p2241fff0} id="Vector_3" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p2c4f400} id="Vector_4" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Container6() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon4 />
    </div>
  );
}

function Text3() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[77.711px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Active Users</p>
    </div>
  );
}

function Container7() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[137.75px]" data-name="Container">
      <Container6 />
      <Text3 />
    </div>
  );
}

function Icon5() {
  return (
    <div className="h-[24px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 48 22">
          <path d={svgPaths.p1d4c6500} fill="var(--fill-0, #990000)" id="Vector" opacity="0.08" />
        </svg>
      </div>
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <div className="absolute inset-[-3.41%_-1.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 50 24">
            <path d={svgPaths.p369d46f0} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[-4.17%_-2%_87.5%_94%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 4 4">
          <path d={svgPaths.p12ed5580} fill="var(--fill-0, #990000)" id="Vector" />
        </svg>
      </div>
    </div>
  );
}

function Container8() {
  return (
    <div className="absolute content-stretch flex flex-col h-[24px] items-start left-[149.75px] top-[4px] w-[50px]" data-name="Container">
      <Icon5 />
    </div>
  );
}

function ChStatCard4() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container7 />
      <Container8 />
    </div>
  );
}

function ChStatCard5() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">892</p>
    </div>
  );
}

function Icon6() {
  return (
    <div className="relative shrink-0 size-[12px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12 12">
        <g id="Icon">
          <path d="M2.5 6L6 2.5L9.5 6" id="Vector" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
          <path d="M6 9.5V2.5" id="Vector_2" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
        </g>
      </svg>
    </div>
  );
}

function Text4() {
  return (
    <div className="basis-0 grow h-[16px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[16px] relative w-full">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] left-0 not-italic text-[#1b5e20] text-[12px] text-nowrap top-[0.5px] whitespace-pre">+12%</p>
      </div>
    </div>
  );
}

function ChStatCard6() {
  return (
    <div className="h-[16px] relative shrink-0 w-[47.43px]" data-name="CHStatCard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[16px] items-center relative w-[47.43px]">
        <Icon6 />
        <Text4 />
      </div>
    </div>
  );
}

function ChBadge1() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[65.43px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center p-px relative w-[65.43px]">
        <ChStatCard6 />
      </div>
    </div>
  );
}

function Text5() {
  return (
    <div className="h-[18px] relative shrink-0 w-[82.508px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[82.508px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">vs last month</p>
      </div>
    </div>
  );
}

function ChStatCard7() {
  return (
    <div className="content-stretch flex gap-[8px] h-[26px] items-center relative shrink-0 w-full" data-name="CHStatCard">
      <ChBadge1 />
      <Text5 />
    </div>
  );
}

function Container9() {
  return (
    <div className="[grid-area:1_/_2] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard4 />
          <ChStatCard5 />
          <ChStatCard7 />
        </div>
      </div>
    </div>
  );
}

function Icon7() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d="M10 5.83333V17.5" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p25713000} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Container10() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon7 />
    </div>
  );
}

function Text6() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[64.156px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Resources</p>
    </div>
  );
}

function Container11() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[137.75px]" data-name="Container">
      <Container10 />
      <Text6 />
    </div>
  );
}

function Icon8() {
  return (
    <div className="h-[24px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 48 22">
          <path d={svgPaths.p12733200} fill="var(--fill-0, #990000)" id="Vector" opacity="0.08" />
        </svg>
      </div>
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <div className="absolute inset-[-3.41%_-1.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 50 24">
            <path d={svgPaths.p13318000} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[-4.17%_-2%_87.5%_94%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 4 4">
          <path d={svgPaths.p12ed5580} fill="var(--fill-0, #990000)" id="Vector" />
        </svg>
      </div>
    </div>
  );
}

function Container12() {
  return (
    <div className="absolute content-stretch flex flex-col h-[24px] items-start left-[149.75px] top-[4px] w-[50px]" data-name="Container">
      <Icon8 />
    </div>
  );
}

function ChStatCard8() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container11 />
      <Container12 />
    </div>
  );
}

function ChStatCard9() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">156</p>
    </div>
  );
}

function Icon9() {
  return (
    <div className="relative shrink-0 size-[12px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12 12">
        <g id="Icon">
          <path d="M2.5 6L6 2.5L9.5 6" id="Vector" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
          <path d="M6 9.5V2.5" id="Vector_2" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
        </g>
      </svg>
    </div>
  );
}

function Text7() {
  return (
    <div className="basis-0 grow h-[16px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[16px] relative w-full">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] left-0 not-italic text-[#1b5e20] text-[12px] text-nowrap top-[0.5px] whitespace-pre">+3</p>
      </div>
    </div>
  );
}

function ChStatCard10() {
  return (
    <div className="h-[16px] relative shrink-0 w-[31.813px]" data-name="CHStatCard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[16px] items-center relative w-[31.813px]">
        <Icon9 />
        <Text7 />
      </div>
    </div>
  );
}

function ChBadge2() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[49.813px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center p-px relative w-[49.813px]">
        <ChStatCard10 />
      </div>
    </div>
  );
}

function Text8() {
  return (
    <div className="h-[18px] relative shrink-0 w-[94.719px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[94.719px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">new this month</p>
      </div>
    </div>
  );
}

function ChStatCard11() {
  return (
    <div className="content-stretch flex gap-[8px] h-[26px] items-center relative shrink-0 w-full" data-name="CHStatCard">
      <ChBadge2 />
      <Text8 />
    </div>
  );
}

function Container13() {
  return (
    <div className="[grid-area:1_/_3] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard8 />
          <ChStatCard9 />
          <ChStatCard11 />
        </div>
      </div>
    </div>
  );
}

function Icon10() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d={svgPaths.p3ac0b600} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p3c797180} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Container14() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon10 />
    </div>
  );
}

function Text9() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[61.164px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Utilization</p>
    </div>
  );
}

function Container15() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[137.75px]" data-name="Container">
      <Container14 />
      <Text9 />
    </div>
  );
}

function Icon11() {
  return (
    <div className="h-[24px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 48 22">
          <path d={svgPaths.p397c7700} fill="var(--fill-0, #990000)" id="Vector" opacity="0.08" />
        </svg>
      </div>
      <div className="absolute inset-[4.17%_2%]" data-name="Vector">
        <div className="absolute inset-[-3.41%_-1.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 50 24">
            <path d={svgPaths.p2785e900} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[-4.17%_-2%_87.5%_94%]" data-name="Vector">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 4 4">
          <path d={svgPaths.p12ed5580} fill="var(--fill-0, #990000)" id="Vector" />
        </svg>
      </div>
    </div>
  );
}

function Container16() {
  return (
    <div className="absolute content-stretch flex flex-col h-[24px] items-start left-[149.75px] top-[4px] w-[50px]" data-name="Container">
      <Icon11 />
    </div>
  );
}

function ChStatCard12() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container15 />
      <Container16 />
    </div>
  );
}

function ChStatCard13() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">87%</p>
    </div>
  );
}

function Icon12() {
  return (
    <div className="relative shrink-0 size-[12px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12 12">
        <g id="Icon">
          <path d="M2.5 6L6 2.5L9.5 6" id="Vector" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
          <path d="M6 9.5V2.5" id="Vector_2" stroke="var(--stroke-0, #1B5E20)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
        </g>
      </svg>
    </div>
  );
}

function Text10() {
  return (
    <div className="basis-0 grow h-[16px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[16px] relative w-full">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] left-0 not-italic text-[#1b5e20] text-[12px] text-nowrap top-[0.5px] whitespace-pre">+5%</p>
      </div>
    </div>
  );
}

function ChStatCard14() {
  return (
    <div className="h-[16px] relative shrink-0 w-[41.789px]" data-name="CHStatCard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[16px] items-center relative w-[41.789px]">
        <Icon12 />
        <Text10 />
      </div>
    </div>
  );
}

function ChBadge3() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[59.789px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center p-px relative w-[59.789px]">
        <ChStatCard14 />
      </div>
    </div>
  );
}

function Text11() {
  return (
    <div className="h-[18px] relative shrink-0 w-[82.508px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[82.508px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">vs last month</p>
      </div>
    </div>
  );
}

function ChStatCard15() {
  return (
    <div className="content-stretch flex gap-[8px] h-[26px] items-center relative shrink-0 w-full" data-name="CHStatCard">
      <ChBadge3 />
      <Text11 />
    </div>
  );
}

function Container17() {
  return (
    <div className="[grid-area:1_/_4] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard12 />
          <ChStatCard13 />
          <ChStatCard15 />
        </div>
      </div>
    </div>
  );
}

function Section1() {
  return (
    <div className="h-[172px] relative shrink-0 w-[1015px]" data-name="Section">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border gap-[16px] grid grid-cols-[repeat(4,_minmax(0px,_1fr))] grid-rows-[repeat(1,_minmax(0px,_1fr))] h-[172px] relative w-[1015px]">
        <Container5 />
        <Container9 />
        <Container13 />
        <Container17 />
      </div>
    </div>
  );
}

function Heading1() {
  return (
    <div className="h-[28px] relative shrink-0 w-full" data-name="Heading 2">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[28px] left-0 not-italic text-[#1e1e1e] text-[20px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">Analytics Overview</p>
    </div>
  );
}

function Paragraph1() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Booking trends and resource distribution</p>
    </div>
  );
}

function Container18() {
  return (
    <div className="content-stretch flex flex-col gap-[4px] h-[50px] items-start relative shrink-0 w-full" data-name="Container">
      <Heading1 />
      <Paragraph1 />
    </div>
  );
}

function ChCardTitle() {
  return (
    <div className="h-[24px] relative shrink-0 w-[174.883px]" data-name="CHCardTitle">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[24px] relative w-[174.883px]">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[24px] left-0 not-italic text-[#1e1e1e] text-[18px] text-nowrap top-0 whitespace-pre">Bookings Over Time</p>
      </div>
    </div>
  );
}

function Icon13() {
  return (
    <div className="h-[16px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute bottom-[37.5%] left-1/2 right-1/2 top-[12.5%]" data-name="Vector">
        <div className="absolute inset-[-8.33%_-0.67px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 2 10">
            <path d="M0.666667 8.66667V0.666667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[62.5%_12.5%_12.5%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-16.67%_-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 6">
            <path d={svgPaths.p59b1b00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[41.67%_29.17%_37.5%_29.17%]" data-name="Vector">
        <div className="absolute inset-[-20%_-10%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 5">
            <path d={svgPaths.p32713180} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Button() {
  return (
    <div className="relative rounded-[12px] shrink-0 size-[32px]" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start pb-0 pt-[8px] px-[8px] relative size-[32px]">
        <Icon13 />
      </div>
    </div>
  );
}

function Text12() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#990000] text-[13px] text-nowrap top-0 whitespace-pre">Details</p>
      </div>
    </div>
  );
}

function Icon14() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M5.25 10.5L8.75 7L5.25 3.5" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Button1() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[18px] items-center relative w-full">
        <Text12 />
        <Icon14 />
      </div>
    </div>
  );
}

function Container19() {
  return (
    <div className="h-[32px] relative shrink-0 w-[99.938px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[32px] items-center relative w-[99.938px]">
        <Button />
        <Button1 />
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="h-[32px] relative shrink-0 w-[457.5px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[32px] items-center justify-between relative w-[457.5px]">
        <ChCardTitle />
        <Container19 />
      </div>
    </div>
  );
}

function ChCardHeader() {
  return (
    <div className="absolute box-border content-stretch flex h-[73px] items-start justify-between left-px pb-px pt-[20px] px-[20px] top-px w-[497.5px]" data-name="CHCardHeader">
      <div aria-hidden="true" className="absolute border-[#eee9e3] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <Dashboard />
    </div>
  );
}

function Group() {
  return (
    <div className="absolute inset-[1.67%_1.09%_11.67%_14.19%]" data-name="Group">
      <div className="absolute bottom-[-0.19%] left-0 right-0 top-[-0.19%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 388 261">
          <g id="Group">
            <path d="M0 260.5H388" id="Vector" stroke="var(--stroke-0, #EEE9E3)" strokeDasharray="3 3" />
            <path d="M0 195.5H388" id="Vector_2" stroke="var(--stroke-0, #EEE9E3)" strokeDasharray="3 3" />
            <path d="M0 130.5H388" id="Vector_3" stroke="var(--stroke-0, #EEE9E3)" strokeDasharray="3 3" />
            <path d="M0 65.5H388" id="Vector_4" stroke="var(--stroke-0, #EEE9E3)" strokeDasharray="3 3" />
            <path d="M0 0.5H388" id="Vector_5" stroke="var(--stroke-0, #EEE9E3)" strokeDasharray="3 3" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group1() {
  return (
    <div className="absolute contents inset-[1.67%_1.09%_11.67%_14.19%]" data-name="Group">
      <Group />
    </div>
  );
}

function RechartsZindex100R1Go() {
  return (
    <div className="absolute contents inset-[1.67%_1.09%_11.67%_14.19%]" data-name="recharts-zindex--100-:r1go:">
      <Group1 />
    </div>
  );
}

function Group2() {
  return (
    <div className="absolute inset-[7.33%_1.09%_11.67%_14.19%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.14%] right-[-0.09%] top-[-0.49%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 389 245">
          <g id="Group">
            <path d={svgPaths.p3c3a7600} fill="var(--fill-0, #990000)" fillOpacity="0.048" id="recharts-area-:r1gq:" />
            <path d={svgPaths.p2cfa3540} id="Vector" stroke="var(--stroke-0, #990000)" strokeWidth="2.5" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group3() {
  return (
    <div className="absolute contents inset-[7.33%_1.09%_11.67%_14.19%]" data-name="Group">
      <Group2 />
    </div>
  );
}

function RechartsZindex100R1Gr() {
  return (
    <div className="absolute contents inset-[7.33%_1.09%_11.67%_14.19%]" data-name="recharts-zindex-100-:r1gr:">
      <Group3 />
    </div>
  );
}

function Group4() {
  return (
    <div className="absolute inset-[88.33%_85.81%_9.67%_14.19%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group5() {
  return (
    <div className="absolute inset-[88.33%_68.86%_9.67%_31.14%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group6() {
  return (
    <div className="absolute inset-[88.33%_51.92%_9.67%_48.08%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group7() {
  return (
    <div className="absolute inset-[88.33%_34.98%_9.67%_65.02%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group8() {
  return (
    <div className="absolute inset-[88.33%_18.03%_9.67%_81.97%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group9() {
  return (
    <div className="absolute inset-[88.33%_1.09%_9.67%_98.91%]" data-name="Group">
      <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 6">
          <g id="Group">
            <path d="M0.5 6V0" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group10() {
  return (
    <div className="absolute contents inset-[88.33%_1.09%_9.67%_14.19%]" data-name="Group">
      <Group4 />
      <Group5 />
      <Group6 />
      <Group7 />
      <Group8 />
      <Group9 />
    </div>
  );
}

function Group11() {
  return (
    <div className="absolute contents inset-[88.33%_1.09%_9.67%_14.19%]" data-name="Group">
      <Group10 />
    </div>
  );
}

function Group12() {
  return (
    <div className="absolute contents inset-[88.33%_1.09%_9.67%_14.19%]" data-name="Group">
      <div className="absolute inset-[88.33%_1.09%_11.67%_14.19%]" data-name="Vector">
        <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 388 1">
            <path d="M0 0.5H388" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </svg>
        </div>
      </div>
      <Group11 />
    </div>
  );
}

function Group13() {
  return (
    <div className="absolute inset-[88.33%_85.81%_11.67%_12.88%]" data-name="Group">
      <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 6 1">
          <g id="Group">
            <path d="M0 0.5H6" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group14() {
  return (
    <div className="absolute inset-[66.67%_85.81%_33.33%_12.88%]" data-name="Group">
      <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 6 1">
          <g id="Group">
            <path d="M0 0.5H6" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group15() {
  return (
    <div className="absolute inset-[45%_85.81%_55%_12.88%]" data-name="Group">
      <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 6 1">
          <g id="Group">
            <path d="M0 0.5H6" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group16() {
  return (
    <div className="absolute inset-[23.33%_85.81%_76.67%_12.88%]" data-name="Group">
      <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 6 1">
          <g id="Group">
            <path d="M0 0.5H6" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group17() {
  return (
    <div className="absolute inset-[1.67%_85.81%_98.33%_12.88%]" data-name="Group">
      <div className="absolute bottom-[-0.5px] left-0 right-0 top-[-0.5px]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 6 1">
          <g id="Group">
            <path d="M0 0.5H6" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group18() {
  return (
    <div className="absolute contents inset-[1.67%_85.81%_11.67%_12.88%]" data-name="Group">
      <Group13 />
      <Group14 />
      <Group15 />
      <Group16 />
      <Group17 />
    </div>
  );
}

function Group19() {
  return (
    <div className="absolute contents inset-[1.67%_85.81%_11.67%_12.88%]" data-name="Group">
      <Group18 />
    </div>
  );
}

function Group20() {
  return (
    <div className="absolute contents inset-[1.67%_85.81%_11.67%_12.88%]" data-name="Group">
      <div className="absolute inset-[1.67%_85.81%_11.67%_14.19%]" data-name="Vector">
        <div className="absolute bottom-0 left-[-0.5px] right-[-0.5px] top-0">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1 260">
            <path d="M0.5 0V260" id="Vector" stroke="var(--stroke-0, #EEE9E3)" />
          </svg>
        </div>
      </div>
      <Group19 />
    </div>
  );
}

function RechartsZindex500R1Gv() {
  return (
    <div className="absolute contents inset-[1.67%_1.09%_9.67%_12.88%]" data-name="recharts-zindex-500-:r1gv:">
      <Group12 />
      <Group20 />
    </div>
  );
}

function Group21() {
  return (
    <div className="absolute inset-[6.33%_0.44%_59%_13.54%]" data-name="Group">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 394 104">
        <g id="Group">
          <path d={svgPaths.p186c2300} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector" />
          <path d={svgPaths.p4329670} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector_2" />
          <path d={svgPaths.p3880180} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector_3" />
          <path d={svgPaths.p2db8500} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector_4" />
          <path d={svgPaths.p3ce43b80} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector_5" />
          <path d={svgPaths.p1bb1080} fill="var(--fill-0, #990000)" fillOpacity="0.6" id="Vector_6" />
        </g>
      </svg>
    </div>
  );
}

function RechartsZindex600R1H() {
  return (
    <div className="absolute contents inset-[6.33%_0.44%_59%_13.54%]" data-name="recharts-zindex-600-:r1h0:">
      <Group21 />
    </div>
  );
}

function Group22() {
  return (
    <div className="absolute contents inset-[89.74%_83.41%_4.92%_11.79%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_83.41%_4.92%_11.79%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">Jan</p>
    </div>
  );
}

function Group23() {
  return (
    <div className="absolute contents inset-[89.74%_66.35%_4.92%_28.62%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_66.35%_4.92%_28.62%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">Feb</p>
    </div>
  );
}

function Group24() {
  return (
    <div className="absolute contents inset-[89.74%_49.3%_4.92%_45.46%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_49.3%_4.92%_45.46%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">Mar</p>
    </div>
  );
}

function Group25() {
  return (
    <div className="absolute contents inset-[89.74%_32.58%_4.92%_62.62%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_32.58%_4.92%_62.62%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">Apr</p>
    </div>
  );
}

function Group26() {
  return (
    <div className="absolute contents inset-[89.74%_15.2%_4.92%_79.13%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_15.2%_4.92%_79.13%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">May</p>
    </div>
  );
}

function Group27() {
  return (
    <div className="absolute contents inset-[89.74%_-0.09%_4.92%_95.06%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[89.74%_-0.09%_4.92%_95.06%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-center text-nowrap whitespace-pre">Jun</p>
    </div>
  );
}

function Group28() {
  return (
    <div className="absolute contents inset-[89.74%_-0.09%_4.92%_11.79%]" data-name="Group">
      <Group22 />
      <Group23 />
      <Group24 />
      <Group25 />
      <Group26 />
      <Group27 />
    </div>
  );
}

function Group29() {
  return (
    <div className="absolute contents inset-[85.54%_87.55%_9.13%_10.48%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[85.54%_87.55%_9.13%_10.48%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-nowrap text-right whitespace-pre">0</p>
    </div>
  );
}

function Group30() {
  return (
    <div className="absolute contents inset-[63.87%_87.55%_30.79%_8.73%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[63.87%_87.55%_30.79%_8.73%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-nowrap text-right whitespace-pre">65</p>
    </div>
  );
}

function Group31() {
  return (
    <div className="absolute contents inset-[42.21%_87.55%_52.46%_7.42%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[42.21%_87.55%_52.46%_7.42%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-nowrap text-right whitespace-pre">130</p>
    </div>
  );
}

function Group32() {
  return (
    <div className="absolute contents inset-[20.54%_87.55%_74.13%_7.42%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[20.54%_87.55%_74.13%_7.42%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-nowrap text-right whitespace-pre">195</p>
    </div>
  );
}

function Group33() {
  return (
    <div className="absolute contents inset-[1.21%_87.55%_93.46%_6.99%]" data-name="Group">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal inset-[1.21%_87.55%_93.46%_6.99%] leading-[normal] not-italic text-[#6b6b6b] text-[13px] text-nowrap text-right whitespace-pre">260</p>
    </div>
  );
}

function Group34() {
  return (
    <div className="absolute contents inset-[1.21%_87.55%_9.13%_6.99%]" data-name="Group">
      <Group29 />
      <Group30 />
      <Group31 />
      <Group32 />
      <Group33 />
    </div>
  );
}

function RechartsZindex2000R1H() {
  return (
    <div className="absolute contents inset-[1.21%_-0.09%_4.92%_6.99%]" data-name="recharts-zindex-2000-:r1h4:">
      <Group28 />
      <Group34 />
    </div>
  );
}

function Icon15() {
  return (
    <div className="absolute h-[300px] left-0 overflow-clip top-0 w-[458px]" data-name="Icon">
      <RechartsZindex100R1Go />
      <RechartsZindex100R1Gr />
      <RechartsZindex500R1Gv />
      <RechartsZindex600R1H />
      <RechartsZindex2000R1H />
    </div>
  );
}

function ChLineChart() {
  return (
    <div className="absolute h-[300px] left-[21px] top-[102px] w-[458px]" data-name="CHLineChart">
      <Icon15 />
    </div>
  );
}

function ChCard() {
  return (
    <div className="[grid-area:1_/_1] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="CHCard">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px] shadow-[0px_1px_0px_0px_rgba(0,0,0,0.02),0px_1px_2px_0px_rgba(0,0,0,0.06)]" />
      <ChCardHeader />
      <ChLineChart />
    </div>
  );
}

function ChCardTitle1() {
  return (
    <div className="h-[24px] relative shrink-0 w-[183.102px]" data-name="CHCardTitle">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[24px] relative w-[183.102px]">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[24px] left-0 not-italic text-[#1e1e1e] text-[18px] text-nowrap top-0 whitespace-pre">Category Breakdown</p>
      </div>
    </div>
  );
}

function Icon16() {
  return (
    <div className="h-[16px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute bottom-[37.5%] left-1/2 right-1/2 top-[12.5%]" data-name="Vector">
        <div className="absolute inset-[-8.33%_-0.67px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 2 10">
            <path d="M0.666667 8.66667V0.666667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[62.5%_12.5%_12.5%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-16.67%_-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 6">
            <path d={svgPaths.p59b1b00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[41.67%_29.17%_37.5%_29.17%]" data-name="Vector">
        <div className="absolute inset-[-20%_-10%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 5">
            <path d={svgPaths.p32713180} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Button2() {
  return (
    <div className="relative rounded-[12px] shrink-0 size-[32px]" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start pb-0 pt-[8px] px-[8px] relative size-[32px]">
        <Icon16 />
      </div>
    </div>
  );
}

function Text13() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#990000] text-[13px] text-nowrap top-0 whitespace-pre">Details</p>
      </div>
    </div>
  );
}

function Icon17() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M5.25 10.5L8.75 7L5.25 3.5" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Button3() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[4px] h-[18px] items-center relative w-full">
        <Text13 />
        <Icon17 />
      </div>
    </div>
  );
}

function Container20() {
  return (
    <div className="h-[32px] relative shrink-0 w-[99.938px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[32px] items-center relative w-[99.938px]">
        <Button2 />
        <Button3 />
      </div>
    </div>
  );
}

function Dashboard1() {
  return (
    <div className="h-[32px] relative shrink-0 w-[457.5px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[32px] items-center justify-between relative w-[457.5px]">
        <ChCardTitle1 />
        <Container20 />
      </div>
    </div>
  );
}

function ChCardHeader1() {
  return (
    <div className="absolute box-border content-stretch flex h-[73px] items-start justify-between left-px pb-px pt-[20px] px-[20px] top-px w-[497.5px]" data-name="CHCardHeader">
      <div aria-hidden="true" className="absolute border-[#eee9e3] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <Dashboard1 />
    </div>
  );
}

function Group35() {
  return (
    <div className="absolute inset-[8.33%_28.17%_58.33%_43.27%]" data-name="Group">
      <div className="absolute inset-[-1%_-0.76%_-1%_-0.96%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 134 102">
          <g id="Group">
            <path d={svgPaths.p40800} fill="var(--fill-0, #990000)" id="Vector" stroke="var(--stroke-0, white)" strokeWidth="2" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group36() {
  return (
    <div className="absolute inset-[9.95%_54.04%_49.47%_28.17%]" data-name="Group">
      <div className="absolute inset-[-1.03%_-1.55%_-1.01%_-1.23%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 84 125">
          <g id="Group">
            <path d={svgPaths.p1e91d200} fill="var(--fill-0, #8B0000)" id="Vector" stroke="var(--stroke-0, white)" strokeWidth="2" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group37() {
  return (
    <div className="absolute bottom-1/4 left-[28.95%] right-[47.76%] top-[46.98%]" data-name="Group">
      <div className="absolute inset-[-1.46%_-1.03%_-1.19%_-1.15%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 109 87">
          <g id="Group">
            <path d={svgPaths.p36715a00} fill="var(--fill-0, #CC3333)" id="Vector" stroke="var(--stroke-0, white)" strokeWidth="2" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group38() {
  return (
    <div className="absolute inset-[52.25%_31.48%_25.18%_51.34%]" data-name="Group">
      <div className="absolute inset-[-2.03%_-1.75%_-1.62%_-1.39%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 82 71">
          <g id="Group">
            <path d={svgPaths.p13047600} fill="var(--fill-0, #E57373)" id="Vector" stroke="var(--stroke-0, white)" strokeWidth="2" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group39() {
  return (
    <div className="absolute inset-[41.67%_28.17%_40.69%_61.11%]" data-name="Group">
      <div className="absolute inset-[-1.89%_-2.04%_-2.6%_-2.81%]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 52 56">
          <g id="Group">
            <path d={svgPaths.p3a1b3680} fill="var(--fill-0, #666666)" id="Vector" stroke="var(--stroke-0, white)" strokeWidth="2" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Group40() {
  return (
    <div className="absolute bottom-1/4 contents left-[28.17%] right-[28.17%] top-[8.33%]" data-name="Group">
      <Group35 />
      <Group36 />
      <Group37 />
      <Group38 />
      <Group39 />
    </div>
  );
}

function Group41() {
  return (
    <div className="absolute bottom-1/4 contents left-[28.17%] right-[28.17%] top-[8.33%]" data-name="Group">
      <Group40 />
    </div>
  );
}

function RechartsZindex100R1H() {
  return (
    <div className="absolute bottom-1/4 contents left-[28.17%] right-[28.17%] top-[8.33%]" data-name="recharts-zindex-100-:r1h8:">
      <Group41 />
    </div>
  );
}

function Icon18() {
  return (
    <div className="absolute h-[300px] left-0 overflow-clip top-0 w-[458px]" data-name="Icon">
      <RechartsZindex100R1H />
    </div>
  );
}

function Container21() {
  return (
    <div className="bg-[#e57373] relative rounded-[1.67772e+07px] shrink-0 size-[12px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border size-[12px]" />
    </div>
  );
}

function Text14() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Conference Rooms</p>
      </div>
    </div>
  );
}

function Container22() {
  return (
    <div className="absolute content-stretch flex gap-[8px] h-[18px] items-center left-[21.59px] top-0 w-[136.914px]" data-name="Container">
      <Container21 />
      <Text14 />
    </div>
  );
}

function Container23() {
  return (
    <div className="bg-[#666666] relative rounded-[1.67772e+07px] shrink-0 size-[12px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border size-[12px]" />
    </div>
  );
}

function Text15() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Equipment</p>
      </div>
    </div>
  );
}

function Container24() {
  return (
    <div className="absolute content-stretch flex gap-[8px] h-[18px] items-center left-[178.5px] top-0 w-[85.469px]" data-name="Container">
      <Container23 />
      <Text15 />
    </div>
  );
}

function Container25() {
  return (
    <div className="bg-[darkred] relative rounded-[1.67772e+07px] shrink-0 size-[12px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border size-[12px]" />
    </div>
  );
}

function Text16() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Labs</p>
      </div>
    </div>
  );
}

function Container26() {
  return (
    <div className="absolute content-stretch flex gap-[8px] h-[18px] items-center left-[283.97px] top-0 w-[49.516px]" data-name="Container">
      <Container25 />
      <Text16 />
    </div>
  );
}

function Container27() {
  return (
    <div className="bg-[#cc3333] relative rounded-[1.67772e+07px] shrink-0 size-[12px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border size-[12px]" />
    </div>
  );
}

function Text17() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Libraries</p>
      </div>
    </div>
  );
}

function Container28() {
  return (
    <div className="absolute content-stretch flex gap-[8px] h-[18px] items-center left-[353.48px] top-0 w-[72.93px]" data-name="Container">
      <Container27 />
      <Text17 />
    </div>
  );
}

function Container29() {
  return (
    <div className="bg-[#990000] relative rounded-[1.67772e+07px] shrink-0 size-[12px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border size-[12px]" />
    </div>
  );
}

function Text18() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Study Rooms</p>
      </div>
    </div>
  );
}

function Container30() {
  return (
    <div className="absolute content-stretch flex gap-[8px] h-[18px] items-center left-[173.3px] top-[26px] w-[101.383px]" data-name="Container">
      <Container29 />
      <Text18 />
    </div>
  );
}

function CustomDoughnutLegend() {
  return (
    <div className="absolute h-[44px] left-[5px] top-[255px] w-[448px]" data-name="CustomDoughnutLegend">
      <Container22 />
      <Container24 />
      <Container26 />
      <Container28 />
      <Container30 />
    </div>
  );
}

function ChDoughnutChart() {
  return (
    <div className="absolute h-[300px] left-[21px] top-[102px] w-[458px]" data-name="CHDoughnutChart">
      <Icon18 />
      <CustomDoughnutLegend />
    </div>
  );
}

function ChCard1() {
  return (
    <div className="[grid-area:1_/_2] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="CHCard">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px] shadow-[0px_1px_0px_0px_rgba(0,0,0,0.02),0px_1px_2px_0px_rgba(0,0,0,0.06)]" />
      <ChCardHeader1 />
      <ChDoughnutChart />
    </div>
  );
}

function Container31() {
  return (
    <div className="gap-[16px] grid grid-cols-[repeat(2,_minmax(0px,_1fr))] grid-rows-[repeat(1,_minmax(0px,_1fr))] h-[423px] relative shrink-0 w-full" data-name="Container">
      <ChCard />
      <ChCard1 />
    </div>
  );
}

function Section2() {
  return (
    <div className="h-[489px] relative shrink-0 w-[1015px]" data-name="Section">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[16px] h-[489px] items-start relative w-[1015px]">
        <Container18 />
        <Container31 />
      </div>
    </div>
  );
}

function Heading2() {
  return (
    <div className="h-[28px] relative shrink-0 w-full" data-name="Heading 2">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[28px] left-0 not-italic text-[#1e1e1e] text-[20px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">Your Activity</p>
    </div>
  );
}

function Paragraph2() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Upcoming bookings and recent actions</p>
    </div>
  );
}

function Container32() {
  return (
    <div className="content-stretch flex flex-col gap-[4px] h-[50px] items-start relative shrink-0 w-full" data-name="Container">
      <Heading2 />
      <Paragraph2 />
    </div>
  );
}

function ChCardTitle2() {
  return (
    <div className="h-[24px] relative shrink-0 w-[174.102px]" data-name="CHCardTitle">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[24px] relative w-[174.102px]">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[24px] left-0 not-italic text-[#1e1e1e] text-[18px] text-nowrap top-0 whitespace-pre">Upcoming Bookings</p>
      </div>
    </div>
  );
}

function Icon19() {
  return (
    <div className="absolute left-[69.88px] size-[14px] top-[7px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M2.91667 7H11.0833" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.pf23dd00} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function ChButton2() {
  return (
    <div className="h-[28px] relative rounded-[8px] shrink-0 w-[95.875px]" data-name="CHButton">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[28px] relative w-[95.875px]">
        <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[16px] left-[12px] not-italic text-[#990000] text-[12px] text-nowrap top-[6.5px] whitespace-pre">View All</p>
        <Icon19 />
      </div>
    </div>
  );
}

function Dashboard2() {
  return (
    <div className="h-[28px] relative shrink-0 w-[457.5px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[28px] items-center justify-between relative w-[457.5px]">
        <ChCardTitle2 />
        <ChButton2 />
      </div>
    </div>
  );
}

function ChCardHeader2() {
  return (
    <div className="absolute box-border content-stretch flex h-[69px] items-start justify-between left-px pb-px pt-[20px] px-[20px] top-px w-[497.5px]" data-name="CHCardHeader">
      <div aria-hidden="true" className="absolute border-[#eee9e3] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <Dashboard2 />
    </div>
  );
}

function Heading3() {
  return (
    <div className="h-[18px] overflow-clip relative shrink-0 w-full" data-name="Heading 4">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Wells Library - Study Room 3A</p>
    </div>
  );
}

function Icon20() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d={svgPaths.p1539e500} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p37b99980} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text19() {
  return (
    <div className="h-[18px] relative shrink-0 w-[128.641px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] overflow-clip relative rounded-[inherit] w-[128.641px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Wells Library, Floor 3</p>
      </div>
    </div>
  );
}

function Container33() {
  return (
    <div className="h-[18px] relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[332.102px]">
        <Icon20 />
        <Text19 />
      </div>
    </div>
  );
}

function Icon21() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M4.66667 1.16667V3.5" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M9.33333 1.16667V3.5" id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p24a2b500} id="Vector_3" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M1.75 5.83333H12.25" id="Vector_4" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text20() {
  return (
    <div className="h-[18px] relative shrink-0 w-[84.563px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[84.563px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Today, Nov 11</p>
      </div>
    </div>
  );
}

function Container34() {
  return (
    <div className="h-[18px] relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[332.102px]">
        <Icon21 />
        <Text20 />
      </div>
    </div>
  );
}

function Icon22() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g clipPath="url(#clip0_3_745)" id="Icon">
          <path d="M7 3.5V7L9.33333 8.16667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.pc012c00} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
        <defs>
          <clipPath id="clip0_3_745">
            <rect fill="white" height="14" width="14" />
          </clipPath>
        </defs>
      </svg>
    </div>
  );
}

function Text21() {
  return (
    <div className="h-[18px] relative shrink-0 w-[116.117px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[116.117px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">2:00 PM - 4:00 PM</p>
      </div>
    </div>
  );
}

function Container35() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-full items-center relative w-[332.102px]">
        <Icon22 />
        <Text21 />
      </div>
    </div>
  );
}

function Container36() {
  return (
    <div className="content-stretch flex flex-col gap-[6px] h-[66px] items-start relative shrink-0 w-full" data-name="Container">
      <Container33 />
      <Container34 />
      <Container35 />
    </div>
  );
}

function Container37() {
  return (
    <div className="basis-0 grow h-[94px] min-h-px min-w-px relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[10px] h-[94px] items-start relative w-full">
        <Heading3 />
        <Container36 />
      </div>
    </div>
  );
}

function ChBadge4() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[79.398px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center px-[9px] py-[5px] relative w-[79.398px]">
        <p className="font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] not-italic relative shrink-0 text-[#1b5e20] text-[12px] text-nowrap whitespace-pre">Confirmed</p>
      </div>
    </div>
  );
}

function Dashboard3() {
  return (
    <div className="content-stretch flex h-[94px] items-start justify-between relative shrink-0 w-full" data-name="Dashboard">
      <Container37 />
      <ChBadge4 />
    </div>
  );
}

function Container38() {
  return (
    <div className="bg-[#f1efec] h-[128px] relative rounded-[16px] shrink-0 w-[457.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[rgba(0,0,0,0)] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col h-[128px] items-start pb-px pt-[17px] px-[17px] relative w-[457.5px]">
        <Dashboard3 />
      </div>
    </div>
  );
}

function Heading4() {
  return (
    <div className="h-[18px] overflow-clip relative shrink-0 w-full" data-name="Heading 4">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Luddy Hall - Lab 2150</p>
    </div>
  );
}

function Icon23() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d={svgPaths.p1539e500} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p37b99980} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text22() {
  return (
    <div className="h-[18px] relative shrink-0 w-[114.898px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] overflow-clip relative rounded-[inherit] w-[114.898px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Luddy Hall, Floor 2</p>
      </div>
    </div>
  );
}

function Container39() {
  return (
    <div className="h-[18px] relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[332.102px]">
        <Icon23 />
        <Text22 />
      </div>
    </div>
  );
}

function Icon24() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M4.66667 1.16667V3.5" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M9.33333 1.16667V3.5" id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p24a2b500} id="Vector_3" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M1.75 5.83333H12.25" id="Vector_4" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text23() {
  return (
    <div className="h-[18px] relative shrink-0 w-[110.078px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[110.078px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Tomorrow, Nov 12</p>
      </div>
    </div>
  );
}

function Container40() {
  return (
    <div className="h-[18px] relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[332.102px]">
        <Icon24 />
        <Text23 />
      </div>
    </div>
  );
}

function Icon25() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g clipPath="url(#clip0_3_745)" id="Icon">
          <path d="M7 3.5V7L9.33333 8.16667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.pc012c00} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
        <defs>
          <clipPath id="clip0_3_745">
            <rect fill="white" height="14" width="14" />
          </clipPath>
        </defs>
      </svg>
    </div>
  );
}

function Text24() {
  return (
    <div className="h-[18px] relative shrink-0 w-[128.508px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[128.508px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">10:00 AM - 12:00 PM</p>
      </div>
    </div>
  );
}

function Container41() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative shrink-0 w-[332.102px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-full items-center relative w-[332.102px]">
        <Icon25 />
        <Text24 />
      </div>
    </div>
  );
}

function Container42() {
  return (
    <div className="content-stretch flex flex-col gap-[6px] h-[66px] items-start relative shrink-0 w-full" data-name="Container">
      <Container39 />
      <Container40 />
      <Container41 />
    </div>
  );
}

function Container43() {
  return (
    <div className="basis-0 grow h-[94px] min-h-px min-w-px relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[10px] h-[94px] items-start relative w-full">
        <Heading4 />
        <Container42 />
      </div>
    </div>
  );
}

function ChBadge5() {
  return (
    <div className="bg-[#e8f5e9] h-[26px] relative rounded-[8px] shrink-0 w-[79.398px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center px-[9px] py-[5px] relative w-[79.398px]">
        <p className="font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] not-italic relative shrink-0 text-[#1b5e20] text-[12px] text-nowrap whitespace-pre">Confirmed</p>
      </div>
    </div>
  );
}

function Dashboard4() {
  return (
    <div className="content-stretch flex h-[94px] items-start justify-between relative shrink-0 w-full" data-name="Dashboard">
      <Container43 />
      <ChBadge5 />
    </div>
  );
}

function Container44() {
  return (
    <div className="bg-[#f1efec] h-[128px] relative rounded-[16px] shrink-0 w-[457.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[rgba(0,0,0,0)] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col h-[128px] items-start pb-px pt-[17px] px-[17px] relative w-[457.5px]">
        <Dashboard4 />
      </div>
    </div>
  );
}

function Heading5() {
  return (
    <div className="h-[18px] overflow-clip relative shrink-0 w-full" data-name="Heading 4">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Student Union - Conference Room B</p>
    </div>
  );
}

function Icon26() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d={svgPaths.p1539e500} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p37b99980} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text25() {
  return (
    <div className="h-[18px] relative shrink-0 w-[137.781px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] overflow-clip relative rounded-[inherit] w-[137.781px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Student Union, Floor 2</p>
      </div>
    </div>
  );
}

function Container45() {
  return (
    <div className="h-[18px] relative shrink-0 w-[345.93px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[345.93px]">
        <Icon26 />
        <Text25 />
      </div>
    </div>
  );
}

function Icon27() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M4.66667 1.16667V3.5" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M9.33333 1.16667V3.5" id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.p24a2b500} id="Vector_3" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d="M1.75 5.83333H12.25" id="Vector_4" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function Text26() {
  return (
    <div className="h-[18px] relative shrink-0 w-[81.18px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[81.18px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Nov 14, 2025</p>
      </div>
    </div>
  );
}

function Container46() {
  return (
    <div className="h-[18px] relative shrink-0 w-[345.93px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[345.93px]">
        <Icon27 />
        <Text26 />
      </div>
    </div>
  );
}

function Icon28() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g clipPath="url(#clip0_3_745)" id="Icon">
          <path d="M7 3.5V7L9.33333 8.16667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.pc012c00} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
        <defs>
          <clipPath id="clip0_3_745">
            <rect fill="white" height="14" width="14" />
          </clipPath>
        </defs>
      </svg>
    </div>
  );
}

function Text27() {
  return (
    <div className="h-[18px] relative shrink-0 w-[114.219px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-[114.219px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">1:00 PM - 3:00 PM</p>
      </div>
    </div>
  );
}

function Container47() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative shrink-0 w-[345.93px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-full items-center relative w-[345.93px]">
        <Icon28 />
        <Text27 />
      </div>
    </div>
  );
}

function Container48() {
  return (
    <div className="content-stretch flex flex-col gap-[6px] h-[66px] items-start relative shrink-0 w-full" data-name="Container">
      <Container45 />
      <Container46 />
      <Container47 />
    </div>
  );
}

function Container49() {
  return (
    <div className="basis-0 grow h-[94px] min-h-px min-w-px relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[10px] h-[94px] items-start relative w-full">
        <Heading5 />
        <Container48 />
      </div>
    </div>
  );
}

function ChBadge6() {
  return (
    <div className="bg-[#fff4e0] h-[26px] relative rounded-[8px] shrink-0 w-[65.57px]" data-name="CHBadge">
      <div aria-hidden="true" className="absolute border border-neutral-200 border-solid inset-0 pointer-events-none rounded-[8px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[26px] items-center justify-center px-[9px] py-[5px] relative w-[65.57px]">
        <p className="font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[16px] not-italic relative shrink-0 text-[#8a5a00] text-[12px] text-nowrap whitespace-pre">Pending</p>
      </div>
    </div>
  );
}

function Dashboard5() {
  return (
    <div className="content-stretch flex h-[94px] items-start justify-between relative shrink-0 w-full" data-name="Dashboard">
      <Container49 />
      <ChBadge6 />
    </div>
  );
}

function Container50() {
  return (
    <div className="basis-0 bg-[#f1efec] grow min-h-px min-w-px relative rounded-[16px] shrink-0 w-[457.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[rgba(0,0,0,0)] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col h-full items-start pb-px pt-[17px] px-[17px] relative w-[457.5px]">
        <Dashboard5 />
      </div>
    </div>
  );
}

function Dashboard6() {
  return (
    <div className="absolute content-stretch flex flex-col gap-[12px] h-[408px] items-start left-[21px] top-[90px] w-[457.5px]" data-name="Dashboard">
      <Container38 />
      <Container44 />
      <Container50 />
    </div>
  );
}

function ChCard2() {
  return (
    <div className="[grid-area:1_/_1] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="CHCard">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px] shadow-[0px_1px_0px_0px_rgba(0,0,0,0.02),0px_1px_2px_0px_rgba(0,0,0,0.06)]" />
      <ChCardHeader2 />
      <Dashboard6 />
    </div>
  );
}

function ChCardTitle3() {
  return (
    <div className="h-[24px] relative shrink-0 w-[132.508px]" data-name="CHCardTitle">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[24px] relative w-[132.508px]">
        <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[24px] left-0 not-italic text-[#1e1e1e] text-[18px] text-nowrap top-0 whitespace-pre">Recent Activity</p>
      </div>
    </div>
  );
}

function Icon29() {
  return (
    <div className="absolute left-[69.88px] size-[14px] top-[7px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Icon">
          <path d="M2.91667 7H11.0833" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
          <path d={svgPaths.pf23dd00} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.16667" />
        </g>
      </svg>
    </div>
  );
}

function ChButton3() {
  return (
    <div className="h-[28px] relative rounded-[8px] shrink-0 w-[95.875px]" data-name="CHButton">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[28px] relative w-[95.875px]">
        <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[16px] left-[12px] not-italic text-[#990000] text-[12px] text-nowrap top-[6.5px] whitespace-pre">View All</p>
        <Icon29 />
      </div>
    </div>
  );
}

function Dashboard7() {
  return (
    <div className="h-[28px] relative shrink-0 w-[457.5px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[28px] items-center justify-between relative w-[457.5px]">
        <ChCardTitle3 />
        <ChButton3 />
      </div>
    </div>
  );
}

function ChCardHeader3() {
  return (
    <div className="absolute box-border content-stretch flex h-[69px] items-start justify-between left-px pb-px pt-[20px] px-[20px] top-px w-[497.5px]" data-name="CHCardHeader">
      <div aria-hidden="true" className="absolute border-[#eee9e3] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <Dashboard7 />
    </div>
  );
}

function Icon30() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M5.33333 1.33333V4" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M10.6667 1.33333V4" id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p3ee34580} id="Vector_3" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M2 6.66667H14" id="Vector_4" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard8() {
  return (
    <div className="relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon30 />
      </div>
    </div>
  );
}

function Text28() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text29() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[46px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">booked</p>
    </div>
  );
}

function Text30() {
  return (
    <div className="absolute h-[18px] left-[76.62px] overflow-clip top-0 w-[189.273px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Wells Library - Study Room 3A</p>
    </div>
  );
}

function Paragraph3() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text28 />
      <Text29 />
      <Text30 />
    </div>
  );
}

function Paragraph4() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">2 minutes ago</p>
    </div>
  );
}

function Dashboard9() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph3 />
        <Paragraph4 />
      </div>
    </div>
  );
}

function Container51() {
  return (
    <div className="h-[51px] relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[0px_0px_1px] border-neutral-200 border-solid inset-0 pointer-events-none rounded-[4px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[51px] items-start pb-px pt-0 px-[4px] relative w-[465.5px]">
        <Dashboard8 />
        <Dashboard9 />
      </div>
    </div>
  );
}

function Icon31() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.pb3a1300} id="Vector" stroke="var(--stroke-0, #8A5A00)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard10() {
  return (
    <div className="bg-[#fff4e0] relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon31 />
      </div>
    </div>
  );
}

function Text31() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text32() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[55.828px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">reviewed</p>
    </div>
  );
}

function Text33() {
  return (
    <div className="absolute h-[18px] left-[86.45px] overflow-clip top-0 w-[135.453px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Luddy Hall - Lab 2150</p>
    </div>
  );
}

function Paragraph5() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text31 />
      <Text32 />
      <Text33 />
    </div>
  );
}

function Paragraph6() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">15 minutes ago</p>
    </div>
  );
}

function Dashboard11() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph5 />
        <Paragraph6 />
      </div>
    </div>
  );
}

function Container52() {
  return (
    <div className="h-[63px] relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[0px_0px_1px] border-neutral-200 border-solid inset-0 pointer-events-none rounded-[4px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[63px] items-start pb-px pt-[12px] px-[4px] relative w-[465.5px]">
        <Dashboard10 />
        <Dashboard11 />
      </div>
    </div>
  );
}

function Icon32() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.p405f80} id="Vector" stroke="var(--stroke-0, #0B5CAD)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard12() {
  return (
    <div className="bg-[#e3f2fd] relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon32 />
      </div>
    </div>
  );
}

function Text34() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text35() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[92.109px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">commented on</p>
    </div>
  );
}

function Text36() {
  return (
    <div className="absolute h-[18px] left-[122.73px] overflow-clip top-0 w-[123.305px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Conference Room B</p>
    </div>
  );
}

function Paragraph7() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text34 />
      <Text35 />
      <Text36 />
    </div>
  );
}

function Paragraph8() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">1 hour ago</p>
    </div>
  );
}

function Dashboard13() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph7 />
        <Paragraph8 />
      </div>
    </div>
  );
}

function Container53() {
  return (
    <div className="h-[63px] relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[0px_0px_1px] border-neutral-200 border-solid inset-0 pointer-events-none rounded-[4px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[63px] items-start pb-px pt-[12px] px-[4px] relative w-[465.5px]">
        <Dashboard12 />
        <Dashboard13 />
      </div>
    </div>
  );
}

function Icon33() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.p399eca00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.pc93b400} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard14() {
  return (
    <div className="bg-[#f1efec] relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon33 />
      </div>
    </div>
  );
}

function Text37() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text38() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[93.555px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">updated profile</p>
    </div>
  );
}

function Text39() {
  return (
    <div className="absolute h-[18px] left-[124.17px] overflow-clip top-0 w-[128.398px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Personal information</p>
    </div>
  );
}

function Paragraph9() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text37 />
      <Text38 />
      <Text39 />
    </div>
  );
}

function Paragraph10() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">2 hours ago</p>
    </div>
  );
}

function Dashboard15() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph9 />
        <Paragraph10 />
      </div>
    </div>
  );
}

function Container54() {
  return (
    <div className="h-[63px] relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[0px_0px_1px] border-neutral-200 border-solid inset-0 pointer-events-none rounded-[4px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[63px] items-start pb-px pt-[12px] px-[4px] relative w-[465.5px]">
        <Dashboard14 />
        <Dashboard15 />
      </div>
    </div>
  );
}

function Icon34() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M5.33333 1.33333V4" id="Vector" stroke="var(--stroke-0, #B71C1C)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M10.6667 1.33333V4" id="Vector_2" stroke="var(--stroke-0, #B71C1C)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p3ee34580} id="Vector_3" stroke="var(--stroke-0, #B71C1C)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M2 6.66667H14" id="Vector_4" stroke="var(--stroke-0, #B71C1C)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard16() {
  return (
    <div className="bg-[#ffebee] relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon34 />
      </div>
    </div>
  );
}

function Text40() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text41() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[58.836px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">cancelled</p>
    </div>
  );
}

function Text42() {
  return (
    <div className="absolute h-[18px] left-[89.45px] overflow-clip top-0 w-[95.758px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Study Room 4B</p>
    </div>
  );
}

function Paragraph11() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text40 />
      <Text41 />
      <Text42 />
    </div>
  );
}

function Paragraph12() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">3 hours ago</p>
    </div>
  );
}

function Dashboard17() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph11 />
        <Paragraph12 />
      </div>
    </div>
  );
}

function Container55() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[0px_0px_1px] border-neutral-200 border-solid inset-0 pointer-events-none rounded-[4px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-full items-start pb-px pt-[12px] px-[4px] relative w-[465.5px]">
        <Dashboard16 />
        <Dashboard17 />
      </div>
    </div>
  );
}

function Icon35() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.p27ba7fa0} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p28db2b80} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Dashboard18() {
  return (
    <div className="bg-[#f1efec] relative rounded-[12px] shrink-0 size-[32px]" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon35 />
      </div>
    </div>
  );
}

function Text43() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-0 top-px w-[23.305px]" data-name="Text">
      <p className="font-['Inter:Medium',sans-serif] font-medium leading-[18px] not-italic relative shrink-0 text-[#1e1e1e] text-[13px] text-nowrap whitespace-pre">You</p>
    </div>
  );
}

function Text44() {
  return (
    <div className="absolute content-stretch flex h-[15.5px] items-start left-[26.96px] top-px w-[53.445px]" data-name="Text">
      <p className="font-['Inter:Regular',sans-serif] font-normal leading-[18px] not-italic relative shrink-0 text-[#6e6e6e] text-[13px] text-nowrap whitespace-pre">changed</p>
    </div>
  );
}

function Text45() {
  return (
    <div className="absolute h-[18px] left-[84.06px] overflow-clip top-0 w-[125.805px]" data-name="Text">
      <p className="absolute font-['Inter:Medium',sans-serif] font-medium leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Notification settings</p>
    </div>
  );
}

function Paragraph13() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <Text43 />
      <Text44 />
      <Text45 />
    </div>
  );
}

function Paragraph14() {
  return (
    <div className="h-[16px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[#999999] text-[12px] text-nowrap top-[0.5px] whitespace-pre">5 hours ago</p>
    </div>
  );
}

function Dashboard19() {
  return (
    <div className="basis-0 grow h-[38px] min-h-px min-w-px relative shrink-0" data-name="Dashboard">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[38px] items-start relative w-full">
        <Paragraph13 />
        <Paragraph14 />
      </div>
    </div>
  );
}

function Container56() {
  return (
    <div className="h-[50px] relative rounded-[4px] shrink-0 w-[465.5px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[12px] h-[50px] items-start pb-0 pt-[12px] px-[4px] relative w-[465.5px]">
        <Dashboard18 />
        <Dashboard19 />
      </div>
    </div>
  );
}

function Dashboard20() {
  return (
    <div className="absolute box-border content-stretch flex flex-col h-[353px] items-start left-[21px] pr-0 py-0 top-[90px] w-[457.5px]" data-name="Dashboard">
      <Container51 />
      <Container52 />
      <Container53 />
      <Container54 />
      <Container55 />
      <Container56 />
    </div>
  );
}

function ChCard3() {
  return (
    <div className="[grid-area:1_/_2] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="CHCard">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px] shadow-[0px_1px_0px_0px_rgba(0,0,0,0.02),0px_1px_2px_0px_rgba(0,0,0,0.06)]" />
      <ChCardHeader3 />
      <Dashboard20 />
    </div>
  );
}

function Container57() {
  return (
    <div className="gap-[16px] grid grid-cols-[repeat(2,_minmax(0px,_1fr))] grid-rows-[repeat(1,_minmax(0px,_1fr))] h-[519px] relative shrink-0 w-full" data-name="Container">
      <ChCard2 />
      <ChCard3 />
    </div>
  );
}

function Section3() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative shrink-0 w-[1015px]" data-name="Section">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[16px] h-full items-start relative w-[1015px]">
        <Container32 />
        <Container57 />
      </div>
    </div>
  );
}

function Heading6() {
  return (
    <div className="h-[28px] relative shrink-0 w-full" data-name="Heading 2">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[28px] left-0 not-italic text-[#1e1e1e] text-[20px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">Quick Stats Summary</p>
    </div>
  );
}

function Paragraph15() {
  return (
    <div className="h-[18px] relative shrink-0 w-full" data-name="Paragraph">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">{`Real-time insights into today's activity`}</p>
    </div>
  );
}

function Container58() {
  return (
    <div className="content-stretch flex flex-col gap-[4px] h-[50px] items-start relative shrink-0 w-full" data-name="Container">
      <Heading6 />
      <Paragraph15 />
    </div>
  );
}

function Icon36() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M5.33333 1.33333V4" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M10.6667 1.33333V4" id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p3ee34580} id="Vector_3" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d="M2 6.66667H14" id="Vector_4" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Container59() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon36 />
    </div>
  );
}

function Text46() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[107.234px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">{`Today's Bookings`}</p>
    </div>
  );
}

function Container60() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[187.75px]" data-name="Container">
      <Container59 />
      <Text46 />
    </div>
  );
}

function Container61() {
  return <div className="absolute left-[199.75px] size-0 top-[4px]" data-name="Container" />;
}

function ChStatCard16() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container60 />
      <Container61 />
    </div>
  );
}

function ChStatCard17() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">24</p>
    </div>
  );
}

function Container62() {
  return (
    <div className="[grid-area:1_/_1] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard16 />
          <ChStatCard17 />
        </div>
      </div>
    </div>
  );
}

function Icon37() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g clipPath="url(#clip0_3_819)" id="Icon">
          <path d="M8 4V8L10.6667 9.33333" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p39ee6532} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
        <defs>
          <clipPath id="clip0_3_819">
            <rect fill="white" height="16" width="16" />
          </clipPath>
        </defs>
      </svg>
    </div>
  );
}

function Container63() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon37 />
    </div>
  );
}

function Text47() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[64.117px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Peak Time</p>
    </div>
  );
}

function ChStatCard18() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container63 />
      <Text47 />
    </div>
  );
}

function ChStatCard19() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">2-4 PM</p>
    </div>
  );
}

function Container64() {
  return (
    <div className="[grid-area:1_/_2] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard18 />
          <ChStatCard19 />
        </div>
      </div>
    </div>
  );
}

function Icon38() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M8 4.66667V14" id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.p8c8fb00} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Container65() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon38 />
    </div>
  );
}

function Text48() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[86px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Available Now</p>
    </div>
  );
}

function ChStatCard20() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container65 />
      <Text48 />
    </div>
  );
}

function ChStatCard21() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">42</p>
    </div>
  );
}

function Container66() {
  return (
    <div className="[grid-area:1_/_3] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard20 />
          <ChStatCard21 />
        </div>
      </div>
    </div>
  );
}

function Icon39() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.p3155f180} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.pea6a680} id="Vector_2" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Container67() {
  return (
    <div className="absolute content-stretch flex items-center justify-center left-0 rounded-[12px] size-[40px] top-0" data-name="Container">
      <Icon39 />
    </div>
  );
}

function Text49() {
  return (
    <div className="absolute h-[18px] left-[50px] top-[4px] w-[82.289px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Avg. Duration</p>
    </div>
  );
}

function Container68() {
  return (
    <div className="absolute h-[40px] left-0 top-0 w-[187.75px]" data-name="Container">
      <Container67 />
      <Text49 />
    </div>
  );
}

function Container69() {
  return <div className="absolute left-[199.75px] size-0 top-[4px]" data-name="Container" />;
}

function ChStatCard22() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <Container68 />
      <Container69 />
    </div>
  );
}

function ChStatCard23() {
  return (
    <div className="h-[40px] relative shrink-0 w-full" data-name="CHStatCard">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">1.8h</p>
    </div>
  );
}

function Container70() {
  return (
    <div className="[grid-area:1_/_4] bg-[#fbfaf9] relative rounded-[16px] shrink-0" data-name="Container">
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="size-full">
        <div className="box-border content-stretch flex flex-col gap-[12px] items-start pb-px pt-[21px] px-[21px] relative size-full">
          <ChStatCard22 />
          <ChStatCard23 />
        </div>
      </div>
    </div>
  );
}

function Container71() {
  return (
    <div className="gap-[16px] grid grid-cols-[repeat(4,_minmax(0px,_1fr))] grid-rows-[repeat(1,_minmax(0px,_1fr))] h-[146px] relative shrink-0 w-full" data-name="Container">
      <Container62 />
      <Container64 />
      <Container66 />
      <Container70 />
    </div>
  );
}

function Section4() {
  return (
    <div className="h-[212px] relative shrink-0 w-[1015px]" data-name="Section">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[16px] h-[212px] items-start relative w-[1015px]">
        <Container58 />
        <Container71 />
      </div>
    </div>
  );
}

function Dashboard21() {
  return (
    <div className="absolute content-stretch flex flex-col gap-[32px] h-[1658px] items-start left-[24px] top-[119px] w-[1015px]" data-name="Dashboard">
      <Header />
      <Section1 />
      <Section2 />
      <Section3 />
      <Section4 />
    </div>
  );
}

function Text50() {
  return (
    <div className="h-[16px] relative shrink-0 w-[12.07px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[16px] relative w-[12.07px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[16px] left-0 not-italic text-[12px] text-nowrap text-white top-[0.5px] whitespace-pre">IU</p>
      </div>
    </div>
  );
}

function Container72() {
  return (
    <div className="bg-[#990000] relative rounded-[4px] shrink-0 size-[24px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center pl-0 pr-[0.008px] py-0 relative size-[24px]">
        <Text50 />
      </div>
    </div>
  );
}

function Text51() {
  return (
    <div className="basis-0 grow h-[20px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[20px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[20px] left-0 not-italic text-[#6e6e6e] text-[14px] text-nowrap top-[0.5px] whitespace-pre">© 2025 Indiana University Campus Resource Hub</p>
      </div>
    </div>
  );
}

function Container73() {
  return (
    <div className="h-[24px] relative shrink-0 w-[360.008px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[24px] items-center relative w-[360.008px]">
        <Container72 />
        <Text51 />
      </div>
    </div>
  );
}

function Link() {
  return (
    <div className="h-[20px] relative shrink-0 w-[100.453px]" data-name="Link">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[20px] relative w-[100.453px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[20px] left-0 not-italic text-[#6e6e6e] text-[14px] text-nowrap top-[0.5px] whitespace-pre">{`Help & Support`}</p>
      </div>
    </div>
  );
}

function Link1() {
  return (
    <div className="h-[20px] relative shrink-0 w-[91.836px]" data-name="Link">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[20px] relative w-[91.836px]">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[20px] left-0 not-italic text-[#6e6e6e] text-[14px] text-nowrap top-[0.5px] whitespace-pre">Privacy Policy</p>
      </div>
    </div>
  );
}

function Link2() {
  return (
    <div className="basis-0 grow h-[20px] min-h-px min-w-px relative shrink-0" data-name="Link">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[20px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[20px] left-0 not-italic text-[#6e6e6e] text-[14px] text-nowrap top-[0.5px] whitespace-pre">Terms of Service</p>
      </div>
    </div>
  );
}

function Container74() {
  return (
    <div className="h-[20px] relative shrink-0 w-[351.914px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[24px] h-[20px] items-center relative w-[351.914px]">
        <Link />
        <Link1 />
        <Link2 />
      </div>
    </div>
  );
}

function Container75() {
  return (
    <div className="content-stretch flex h-[24px] items-center justify-between relative shrink-0 w-full" data-name="Container">
      <Container73 />
      <Container74 />
    </div>
  );
}

function Footer() {
  return (
    <div className="absolute bg-[#fbfaf9] box-border content-stretch flex flex-col h-[73px] items-start left-0 pb-0 pt-[25px] px-[24px] top-[1801px] w-[1063px]" data-name="Footer">
      <div aria-hidden="true" className="absolute border-[#e9e4dd] border-[1px_0px_0px] border-solid inset-0 pointer-events-none" />
      <Container75 />
    </div>
  );
}

function Container76() {
  return (
    <div className="basis-0 grow h-[1874px] min-h-px min-w-px relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[1874px] relative w-full">
        <Dashboard21 />
        <Footer />
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="absolute bg-[#f9f7f6] content-stretch flex gap-[72px] h-[1874px] items-start left-0 top-0 w-[1135px]" data-name="App">
      <Section />
      <Container76 />
    </div>
  );
}

function Group42() {
  return (
    <div className="absolute inset-[12.5%_21.88%]" data-name="Group">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 18">
        <g id="Group">
          <path d={svgPaths.p37516e00} fill="var(--fill-0, #990000)" id="Vector" />
          <path d={svgPaths.p13be6700} fill="var(--fill-0, #990000)" id="Vector_2" />
          <path d={svgPaths.p14fdfe00} fill="var(--fill-0, #990000)" id="Vector_3" />
          <path d="M3 3.75H0V5.25H3V3.75Z" fill="var(--fill-0, #990000)" id="Vector_4" />
          <path d={svgPaths.p2d878700} fill="var(--fill-0, #990000)" id="Vector_5" />
          <path d="M3 12.75H0V14.25H3V12.75Z" fill="var(--fill-0, #990000)" id="Vector_6" />
          <path d={svgPaths.p384c1300} fill="var(--fill-0, #990000)" id="Vector_7" />
        </g>
      </svg>
    </div>
  );
}

function IuLogo() {
  return (
    <div className="relative shrink-0 size-[24px]" data-name="IULogo">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border overflow-clip relative rounded-[inherit] size-[24px]">
        <Group42 />
      </div>
    </div>
  );
}

function Container77() {
  return (
    <div className="h-[57px] relative shrink-0 w-[71px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[#e9e4dd] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[57px] items-center justify-center pb-px pt-0 px-0 relative w-[71px]">
        <IuLogo />
      </div>
    </div>
  );
}

function Icon40() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute bottom-1/2 left-[12.5%] right-[58.33%] top-[12.5%]" data-name="Vector">
        <div className="absolute inset-[-11.11%_-14.29%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 10">
            <path d={svgPaths.p16a0fc00} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[12.5%_12.5%_66.67%_58.33%]" data-name="Vector">
        <div className="absolute inset-[-20%_-14.29%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 6">
            <path d={svgPaths.p33770900} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute bottom-[12.5%] left-[58.33%] right-[12.5%] top-1/2" data-name="Vector">
        <div className="absolute inset-[-11.11%_-14.29%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 10">
            <path d={svgPaths.p16a0fc00} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[66.67%_58.33%_12.5%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-20%_-14.29%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 8 6">
            <path d={svgPaths.p33770900} id="Vector" stroke="var(--stroke-0, #990000)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text52() {
  return (
    <div className="absolute content-stretch flex flex-col items-start left-[16px] size-[20px] top-[10px]" data-name="Text">
      <Icon40 />
    </div>
  );
}

function Container78() {
  return <div className="absolute bg-[#990000] h-[20px] left-0 rounded-br-[20px] rounded-tr-[20px] top-[10px] w-[4px]" data-name="Container" />;
}

function Button4() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <Text52 />
      <Container78 />
    </div>
  );
}

function Icon41() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[8.34%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-5%_-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 19">
            <path d={svgPaths.p3d7c0300} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute bottom-[8.33%] left-1/2 right-1/2 top-1/2" data-name="Vector">
        <div className="absolute inset-[-10%_-0.83px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 2 10">
            <path d="M0.833333 9.16667V0.833333" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute bottom-1/2 left-[13.71%] right-[13.71%] top-[29.17%]" data-name="Vector">
        <div className="absolute inset-[-20%_-5.74%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 6">
            <path d={svgPaths.p3049b800} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[17.79%_31.25%_60.75%_31.25%]" data-name="Vector">
        <div className="absolute inset-[-19.42%_-11.11%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 10 6">
            <path d={svgPaths.p16398ce0} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text53() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon41 />
      </div>
    </div>
  );
}

function Button5() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text53 />
        </div>
      </div>
    </div>
  );
}

function Icon42() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute bottom-3/4 left-[33.33%] right-[66.67%] top-[8.33%]" data-name="Vector">
        <div className="absolute inset-[-25%_-0.83px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 2 5">
            <path d="M0.833333 0.833333V4.16667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute bottom-3/4 left-[66.67%] right-[33.33%] top-[8.33%]" data-name="Vector">
        <div className="absolute inset-[-25%_-0.83px]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 2 5">
            <path d="M0.833333 0.833333V4.16667" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[16.67%_12.5%_8.33%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 17">
            <path d={svgPaths.pf3beb80} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[41.67%_12.5%_58.33%_12.5%]" data-name="Vector">
        <div className="absolute inset-[-0.83px_-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 2">
            <path d="M0.833333 0.833333H15.8333" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text54() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon42 />
      </div>
    </div>
  );
}

function Button6() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text54 />
        </div>
      </div>
    </div>
  );
}

function Icon43() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[12.5%_8.33%_8.35%_8.33%]" data-name="Vector">
        <div className="absolute inset-[-5.26%_-5%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 19 18">
            <path d={svgPaths.p190f2380} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text55() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon43 />
      </div>
    </div>
  );
}

function Button7() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text55 />
        </div>
      </div>
    </div>
  );
}

function Icon44() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[8.33%_8.33%_12.2%_8.33%]" data-name="Vector">
        <div className="absolute inset-[-5.24%_-5%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 19 18">
            <path d={svgPaths.p31c92d00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text56() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon44 />
      </div>
    </div>
  );
}

function Button8() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text56 />
        </div>
      </div>
    </div>
  );
}

function Icon45() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[8.33%_16.67%_8.32%_16.67%]" data-name="Vector">
        <div className="absolute inset-[-5%_-6.25%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 15 19">
            <path d={svgPaths.p30439e00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text57() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon45 />
      </div>
    </div>
  );
}

function Button9() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text57 />
        </div>
      </div>
    </div>
  );
}

function Icon46() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[12.5%]" data-name="Vector">
        <div className="absolute inset-[-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 17">
            <path d={svgPaths.p2a35e580} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text58() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon46 />
      </div>
    </div>
  );
}

function Button10() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text58 />
        </div>
      </div>
    </div>
  );
}

function Icon47() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[8.41%_12.68%]" data-name="Vector">
        <div className="absolute inset-[-5.01%_-5.58%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 19">
            <path d={svgPaths.p2322a380} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
      <div className="absolute inset-[37.5%]" data-name="Vector">
        <div className="absolute inset-[-16.67%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 7 7">
            <path d={svgPaths.p2314a170} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Text59() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col items-start relative size-[20px]">
        <Icon47 />
      </div>
    </div>
  );
}

function Button11() {
  return (
    <div className="h-[40px] relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[40px] items-center pl-[16px] pr-0 py-0 relative w-full">
          <Text59 />
        </div>
      </div>
    </div>
  );
}

function Navigation() {
  return (
    <div className="basis-0 grow min-h-px min-w-px relative shrink-0 w-[71px]" data-name="Navigation">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-full items-start overflow-clip pb-0 pt-[12px] px-[12px] relative rounded-[inherit] w-[71px]">
        <Button4 />
        <Button5 />
        <Button6 />
        <Button7 />
        <Button8 />
        <Button9 />
        <Button10 />
        <Button11 />
      </div>
    </div>
  );
}

function Icon48() {
  return (
    <div className="relative shrink-0 size-[15px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 15 15">
        <g id="Icon">
          <path d={svgPaths.p5646280} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.25" />
        </g>
      </svg>
    </div>
  );
}

function Button12() {
  return (
    <div className="content-stretch flex h-[40px] items-center justify-center relative rounded-[12px] shrink-0 w-full" data-name="Button">
      <Icon48 />
    </div>
  );
}

function Container79() {
  return (
    <div className="h-[65px] relative shrink-0 w-[71px]" data-name="Container">
      <div aria-hidden="true" className="absolute border-[#e9e4dd] border-[1px_0px_0px] border-solid inset-0 pointer-events-none" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col h-[65px] items-start pb-0 pt-[13px] px-[12px] relative w-[71px]">
        <Button12 />
      </div>
    </div>
  );
}

function Sidebar() {
  return (
    <div className="absolute bg-[#fbfaf9] box-border content-stretch flex flex-col h-[836px] items-start left-0 pl-0 pr-px py-0 top-0 w-[72px]" data-name="Sidebar">
      <div aria-hidden="true" className="absolute border-[#e9e4dd] border-[0px_1px_0px_0px] border-solid inset-0 pointer-events-none" />
      <Container77 />
      <Navigation />
      <Container79 />
    </div>
  );
}

function Text60() {
  return (
    <div className="absolute h-[24px] left-0 top-[-20000px] w-[8.125px]" data-name="Text">
      <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[24px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">0</p>
    </div>
  );
}

function Text61() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Home</p>
      </div>
    </div>
  );
}

function ListItem() {
  return (
    <div className="h-[18px] relative shrink-0 w-[36.25px]" data-name="List Item">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex h-[18px] items-center relative w-[36.25px]">
        <Text61 />
      </div>
    </div>
  );
}

function Icon49() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d="M6 12L10 8L6 4" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Text62() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#1e1e1e] text-[13px] text-nowrap top-0 whitespace-pre">Dashboard</p>
      </div>
    </div>
  );
}

function ListItem1() {
  return (
    <div className="h-[18px] relative shrink-0 w-[91px]" data-name="List Item">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex gap-[8px] h-[18px] items-center relative w-[91px]">
        <Icon49 />
        <Text62 />
      </div>
    </div>
  );
}

function NumberedList() {
  return (
    <div className="content-stretch flex gap-[8px] h-[18px] items-center relative shrink-0 w-full" data-name="Numbered List">
      <ListItem />
      <ListItem1 />
    </div>
  );
}

function Heading7() {
  return (
    <div className="h-[40px] overflow-clip relative shrink-0 w-full" data-name="Heading 1">
      <p className="absolute font-['Inter:Semi_Bold',sans-serif] font-semibold leading-[40px] left-0 not-italic text-[#1e1e1e] text-[32px] text-nowrap top-[-0.5px] tracking-[-0.2px] whitespace-pre">Dashboard</p>
    </div>
  );
}

function Container80() {
  return (
    <div className="basis-0 grow h-[62px] min-h-px min-w-px relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex flex-col gap-[4px] h-[62px] items-start relative w-full">
        <NumberedList />
        <Heading7 />
      </div>
    </div>
  );
}

function Icon50() {
  return (
    <div className="h-[20px] overflow-clip relative shrink-0 w-full" data-name="Icon">
      <div className="absolute inset-[12.56%_12.56%_12.5%_12.49%]" data-name="Vector">
        <div className="absolute inset-[-5.56%]">
          <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17 17">
            <path d={svgPaths.p11067680} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          </svg>
        </div>
      </div>
    </div>
  );
}

function Button13() {
  return (
    <div className="absolute box-border content-stretch flex flex-col items-start left-[388px] pb-0 pt-[8px] px-[8px] rounded-[12px] size-[36px] top-[2px]" data-name="Button">
      <Icon50 />
    </div>
  );
}

function SearchInput() {
  return (
    <div className="absolute bg-[#fbfaf9] h-[36px] left-0 rounded-[12px] top-0 w-[320px]" data-name="Search Input">
      <div className="box-border content-stretch flex h-[36px] items-center overflow-clip pl-[40px] pr-[16px] py-[8px] relative rounded-[inherit] w-[320px]">
        <p className="font-['Inter:Regular',sans-serif] font-normal leading-[normal] not-italic relative shrink-0 text-[13px] text-[rgba(110,110,110,0.5)] text-nowrap whitespace-pre">Search resources, bookings...</p>
      </div>
      <div aria-hidden="true" className="absolute border border-[#e9e4dd] border-solid inset-0 pointer-events-none rounded-[12px]" />
    </div>
  );
}

function Icon51() {
  return (
    <div className="absolute left-[12px] size-[20px] top-[8px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d="M17.5 17.5L13.8833 13.8833" id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.pcddfd00} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Container81() {
  return (
    <div className="absolute h-[36px] left-0 top-[2px] w-[320px]" data-name="Container">
      <SearchInput />
      <Icon51 />
    </div>
  );
}

function Icon52() {
  return (
    <div className="absolute left-[8px] size-[20px] top-[8px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
        <g id="Icon">
          <path d={svgPaths.p3b7be120} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
          <path d={svgPaths.p1f3d9f80} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.66667" />
        </g>
      </svg>
    </div>
  );
}

function Text63() {
  return (
    <div className="absolute left-[24px] rounded-[1.67772e+07px] size-[8px] top-[4px]" data-name="Text">
      <div aria-hidden="true" className="absolute border-2 border-neutral-200 border-solid inset-0 pointer-events-none rounded-[1.67772e+07px]" />
    </div>
  );
}

function Button14() {
  return (
    <div className="absolute left-[336px] rounded-[12px] size-[36px] top-[2px]" data-name="Button">
      <Icon52 />
      <Text63 />
    </div>
  );
}

function Icon53() {
  return (
    <div className="relative shrink-0 size-[16px]" data-name="Icon">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Icon">
          <path d={svgPaths.p399eca00} id="Vector" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
          <path d={svgPaths.pc93b400} id="Vector_2" stroke="var(--stroke-0, #6E6E6E)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.33333" />
        </g>
      </svg>
    </div>
  );
}

function Container82() {
  return (
    <div className="bg-[#990000] relative rounded-[1.67772e+07px] shrink-0 size-[32px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border content-stretch flex items-center justify-center relative size-[32px]">
        <Icon53 />
      </div>
    </div>
  );
}

function Text64() {
  return (
    <div className="basis-0 grow h-[18px] min-h-px min-w-px relative shrink-0" data-name="Text">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[18px] relative w-full">
        <p className="absolute font-['Inter:Regular',sans-serif] font-normal leading-[18px] left-0 not-italic text-[#6e6e6e] text-[13px] text-nowrap top-0 whitespace-pre">Admin User</p>
      </div>
    </div>
  );
}

function Button15() {
  return (
    <div className="absolute box-border content-stretch flex gap-[8px] h-[40px] items-center left-[440px] px-[4px] py-0 rounded-[16px] top-0 w-[119.359px]" data-name="Button">
      <Container82 />
      <Text64 />
    </div>
  );
}

function Container83() {
  return (
    <div className="h-[40px] relative shrink-0 w-[559.359px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid box-border h-[40px] relative w-[559.359px]">
        <Button13 />
        <Container81 />
        <Button14 />
        <Button15 />
      </div>
    </div>
  );
}

function Container84() {
  return (
    <div className="h-[94px] relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-row items-center size-full">
        <div className="box-border content-stretch flex h-[94px] items-center justify-between px-[20px] py-0 relative w-full">
          <Container80 />
          <Container83 />
        </div>
      </div>
    </div>
  );
}

function Topbar() {
  return (
    <div className="absolute bg-[#fbfaf9] box-border content-stretch flex flex-col h-[95px] items-start left-[72px] pb-px pt-0 px-0 top-0 w-[1063px]" data-name="Topbar">
      <div aria-hidden="true" className="absolute border-[#e9e4dd] border-[0px_0px_1px] border-solid inset-0 pointer-events-none" />
      <Container84 />
    </div>
  );
}

export default function CampusResourceHubAdminPanel() {
  return (
    <div className="bg-[#f9f7f6] relative size-full" data-name="Campus Resource Hub- Admin Panel">
      <App />
      <Sidebar />
      <Text60 />
      <Topbar />
    </div>
  );
}