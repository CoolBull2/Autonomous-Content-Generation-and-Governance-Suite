from langchain_openai import OpenAI
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any, List
from langchain_perplexity import ChatPerplexity
import re
import os
from ..base_agent import BaseAgent
from dotenv import load_dotenv
load_dotenv()


class FactualityAgent(BaseAgent):
    """Agent responsible for fact-checking and compliance verification"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("FactualityChecker", config)

        self.llm = ChatPerplexity(
            model="sonar-pro",
            temperature=0.1,  # Low temperature for factual accuracy
            api_key=os.getenv("PPLX_API_KEY")  # Use api_key parameter
        )
        self.compliance_rules = self._load_compliance_rules()

    def _load_compliance_rules(self) -> Dict[str, List[str]]:
        """Load compliance rules for different regulations"""
        return {
            "gdpr": [
                "no personal data without consent",
                "right to be forgotten",
                "data portability"
            ],
            "ccpa": [
                "right to know about data collection",
                "right to delete personal information",
                "right to non-discrimination"
            ],
            "general": [
                "no false claims",
                "accurate statistics",
                "proper attribution"
            ]
        }

    def process(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Check content for factual accuracy and compliance"""
        try:
            self.log_activity("Starting factuality check", {
                "content_length": len(content.get("content", ""))
            })

            text_content = content.get("content", "")
            # Perform fact-checking
            
            fact_check_results = self._check_facts(text_content)
            
            # Check compliance
            compliance_results = self._check_compliance(text_content)

            # Calculate overall score
            overall_score = self._calculate_factuality_score(
                fact_check_results, compliance_results
            )

            result = {
                "fact_check": fact_check_results,
                "compliance": compliance_results,
                "overall_score": overall_score,
                "status": "passed" if overall_score > 0.7 else "failed",
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }

            self.log_activity("Factuality check completed", {
                "score": overall_score,
                "status": result["status"]
            })

            return result

        except Exception as e:
            self.log_activity("Factuality check failed", {"error": str(e)})
            return {
                "error": str(e),
                "status": "error"
            }

    def _check_facts(self, content: str) -> Dict[str, Any]:
        """Check factual claims in the content"""
        # Extract potential factual claims
        claims = self._extract_claims(content)
        
        fact_check_prompt = PromptTemplate(
            input_variables=["claims"],
            template="""
            You are a fact-checker. Analyze the following claims for accuracy:
            
            Claims: {claims}
            
            For each claim, determine:
            1. Is it factually accurate?
            2. Can it be verified?
            3. Are there any red flags?
            
            Rate each claim as: ACCURATE, QUESTIONABLE, or INACCURATE
            Provide reasoning for each rating.
            
            Response format:
            Claim 1: [RATING] - [Reasoning]
            Claim 2: [RATING] - [Reasoning]
            """
        )

        # chain = LLMChain(llm=self.llm, prompt=fact_check_prompt)
        runnable = fact_check_prompt | self.llm
        if claims:
            # fact_check_response = chain.run(claims="\n".join(claims))
            fact_check_response = runnable.invoke(
                {"claims": "\n".join(claims)})
            return {
                "claims_found": len(claims),
                "analysis": fact_check_response,
                "flagged_claims": self._parse_flagged_claims(fact_check_response)
            }
                
        else:
            return {
                "claims_found": 0,
                "analysis": "No specific factual claims detected",
                "flagged_claims": []
            }

    def _extract_claims(self, content: str) -> List[str]:
        """Extract potential factual claims from content"""
        # Simple pattern matching for claims
        patterns = [
            # Existing patterns
            r"(\d+% of .+)",  # Percentage claims
            r"(studies show .+)",  # Research claims
            r"(according to .+)",  # Attribution claims
            r"(research indicates .+)",  # Research claims

            # Statistical and numerical claims
            r"(\d+ out of \d+ .+)",  # Ratio claims
            r"(\d+x more .+)",  # Multiplier claims
            r"(up to \d+% .+)",  # Range percentage claims
            r"(over \d+.+ .+)",  # "Over X" claims
            r"(more than \d+ .+)",  # "More than X" claims
            r"(\d+ times .+)",  # "X times" claims
            r"(nearly \d+% .+)",  # "Nearly X%" claims
            r"(approximately \d+ .+)",  # Approximation claims

            # Expert and authority claims
            r"(experts say .+)",  # Expert opinions
            r"(scientists found .+)",  # Scientific findings
            r"(researchers discovered .+)",  # Research discoveries
            r"(data shows .+)",  # Data-based claims
            r"(analysis reveals .+)",  # Analysis results
            r"(survey found .+)",  # Survey results
            r"(report shows .+)",  # Report findings
            r"(clinical trials .+)",  # Medical research
            r"(peer-reviewed .+)",  # Academic validation

            # Temporal and trend claims
            r"(in recent years .+)",  # Time-based claims
            r"(latest research .+)",  # Recent findings
            r"(new study .+)",  # New research
            r"(recent data .+)",  # Recent information
            r"(breakthrough study .+)",  # Significant research

            # Comparative claims
            r"(compared to .+)",  # Comparison statements
            r"(better than .+)",  # Superior claims
            r"(faster than .+)",  # Speed comparisons
            r"(more effective than .+)",  # Effectiveness claims
            r"(proven to be .+)",  # Proof claims

            # Certainty and probability
            r"(proven fact .+)",  # Certainty claims
            r"(guaranteed to .+)",  # Guarantee statements
            r"(scientifically proven .+)",  # Scientific validation
            r"(clinically proven .+)",  # Medical validation
            r"(evidence suggests .+)",  # Evidence-based claims
            r"(shown to .+)",  # Demonstration claims

            # Source attribution
            r"(published in .+)",  # Publication references
            r"(featured in .+)",  # Media mentions
            r"(as reported by .+)",  # Media attribution
            r"(cited by .+)",  # Citation references
            r"(recommended by .+)",  # Endorsement claims

            # Health and medical claims
            r"(doctors recommend .+)",  # Medical recommendations
            r"(fda approved .+)",  # Regulatory approval
            r"(clinically tested .+)",  # Testing claims
            r"(medical professionals .+)",  # Professional opinions

            # Business and market claims
            r"(market leader .+)",  # Market position
            r"(industry standard .+)",  # Standard claims
            r"(award-winning .+)",  # Recognition claims
            r"(bestselling .+)",  # Sales claims
            r"(top-rated .+)",  # Rating claims

            # User and customer claims
            r"(customers report .+)",  # Customer feedback
            r"(users experience .+)",  # User experience
            r"(testimonials show .+)",  # Testimonial claims
            r"(reviews indicate .+)",  # Review-based claims

            # Superlative and absolute claims
            r"(world's first .+)",  # Innovation claims
            r"(only .+ that .+)",  # Exclusivity claims
            r"(never before .+)",  # Novelty claims
            r"(revolutionary .+)",  # Revolutionary claims
            r"(breakthrough .+)",  # Breakthrough claims
            r"(cutting-edge .+)",  # Technology claims
        ]

        claims = []
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                claims.append(match.group(1))

        return claims

    def _check_compliance(self, content: str) -> Dict[str, Any]:
        """Check content for regulatory compliance"""
        violations = []

        # Check for potential GDPR violations
        if re.search(r"personal data|email address|phone number", content, re.IGNORECASE):
            if "consent" not in content.lower():
                violations.append(
                    "Potential GDPR violation: Personal data mentioned without consent reference")

        # Check for unsubstantiated claims
        if re.search(r"guaranteed|100% effective|never fails", content, re.IGNORECASE):
            violations.append("Absolute claims that may be misleading")

        # Check for proper attribution
        if re.search(r"studies show|research indicates", content, re.IGNORECASE):
            if not re.search(r"according to|source:|citation", content, re.IGNORECASE):
                violations.append("Research claims without proper attribution")

        return {
            "violations": violations,
            "compliance_score": 1.0 - (len(violations) * 0.2),
            "status": "compliant" if len(violations) == 0 else "non-compliant"
        }

    def _parse_flagged_claims(self, analysis: str) -> List[str]:
        """Parse flagged claims from fact-check analysis"""
        flagged = []
        lines = analysis.content.split('\n')
        for line in lines:
            if 'QUESTIONABLE' in line or 'INACCURATE' in line:
                flagged.append(line.strip())

        return flagged

    def _calculate_factuality_score(self, fact_check: Dict, compliance: Dict) -> float:
        """Calculate overall factuality score"""
        fact_score = 1.0 - (len(fact_check.get("flagged_claims", [])) * 0.3)
        compliance_score = compliance.get("compliance_score", 0.0)

        return (fact_score + compliance_score) / 2
